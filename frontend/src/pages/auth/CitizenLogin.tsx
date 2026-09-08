import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  ShieldCheck,
  UserRound,
  MapPin,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { useLogin } from "../../features/auth/hooks/useLogin";
import { useCitizenOtpRegistration } from "../../features/auth/hooks/useCitizenOtpRegistration";
import {
  useRequestPasswordReset,
  useVerifyPasswordResetOtp,
  useResetPassword,
  useRequestUsernameRecovery,
  useVerifyUsernameRecoveryOtp,
} from "../../features/auth/hooks/useAccountRecovery";

import {
  useDistricts,
  useTehsils,
  useBlocks,
  useMunicipalBodies,
  useWards,
  useLocalities,
  useGramPanchayatsByBlock,
  useVillagesByGramPanchayat,
} from "../../features/government/hooks/useGovernmentData";

import "./CitizenLogin.css";

export function CitizenLogin() {
  const navigate = useNavigate();

  const loginMutation = useLogin();
  const {
  requestOtpMutation,
  verifyOtpMutation,
} = useCitizenOtpRegistration();

  const [mode, setMode] = useState<"signin" | "register">(
    "signin",
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [recoveryMode, setRecoveryMode] =
    useState<"password" | "username" | null>(null);

  const [recoveryStep, setRecoveryStep] = useState<
    "identifier" | "otp" | "reset" | "success"
  >("identifier");

  const [recoveryIdentifier, setRecoveryIdentifier] =
    useState("");

  const [recoveryId, setRecoveryId] =
    useState<number | null>(null);

  const [recoveryOtp, setRecoveryOtp] =
    useState("");

  const [recoveryNewPassword, setRecoveryNewPassword] =
    useState("");

  const [recoveryConfirmPassword, setRecoveryConfirmPassword] =
    useState("");

  const requestPasswordResetMutation =
    useRequestPasswordReset();

  const verifyPasswordResetOtpMutation =
    useVerifyPasswordResetOtp();

  const resetPasswordMutation =
    useResetPassword();

  const requestUsernameRecoveryMutation =
    useRequestUsernameRecovery();

  const verifyUsernameRecoveryOtpMutation =
    useVerifyUsernameRecoveryOtp();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");

  const [registrationId, setRegistrationId] =
    useState<number | null>(null);

  const [otp, setOtp] = useState("");

  const [otpSent, setOtpSent] =
    useState(false);

  const [mobileVerified, setMobileVerified] =
    useState(false);

  const [fatherName, setFatherName] = useState("");
  const [motherName, setMotherName] = useState("");
  const [gender, setGender] = useState("");
  const [dob, setDob] = useState("");

  const [areaType, setAreaType] = useState<
    "rural" | "urban"
  >("rural");

  const [districtId, setDistrictId] =
    useState<number | "">("");

  const [tehsilId, setTehsilId] =
    useState<number | "">("");

  const [blockId, setBlockId] =
    useState<number | "">("");

  const [gramPanchayatId, setGramPanchayatId] =
    useState<number | "">("");

  const [villageId, setVillageId] =
    useState<number | "">("");

  const [municipalBodyType, setMunicipalBodyType] =
    useState<
      | ""
      | "NAGAR_NIGAM"
      | "NAGAR_PALIKA_PARISHAD"
      | "NAGAR_PANCHAYAT"
      | "NOTIFIED_AREA_COUNCIL"
      | "CANTONMENT_BOARD"
    >("");

  const [municipalBodyId, setMunicipalBodyId] =
    useState<number | "">("");

  const [wardId, setWardId] =
    useState<number | "">("");

  const [address, setAddress] = useState("");
  const [pincode, setPincode] = useState("");

  const { data: districts = [] } =
    useDistricts();

  const { data: tehsils = [] } =
    useTehsils();

  const { data: blocks = [] } =
    useBlocks();

  const {
    data: gramPanchayats = [],
    isLoading: isGramPanchayatsLoading,
  } = useGramPanchayatsByBlock(
    blockId,
  );

  const {
    data: villages = [],
    isLoading: isVillagesLoading,
  } = useVillagesByGramPanchayat(
    gramPanchayatId,
  );

  console.log("GP DEBUG", {
    districtId,
    tehsilId,
    blockId,
    gramPanchayatsCount:
      gramPanchayats.length,
    darbePur: gramPanchayats.find(
      (item) =>
        item.gram_panchayat_name
          .toLowerCase() ===
        "darbepur",
    ),
  });

  const { data: municipalBodies = [] } =
    useMunicipalBodies();

  const { data: wards = [] } =
    useWards();

  const { data: localities = [] } =
    useLocalities();

  const filteredTehsils = useMemo(
    () =>
      districtId === ""
        ? []
        : tehsils.filter(
            (item) =>
              item.district_id === districtId,
          ),
    [districtId, tehsils],
  );

  const filteredBlocks = useMemo(
    () =>
      tehsilId === ""
        ? []
        : blocks.filter(
            (item) =>
              Array.isArray(item.tehsil_ids) &&
              item.tehsil_ids.includes(tehsilId),
          ),
    [tehsilId, blocks],
  );

  const availableMunicipalBodyTypes = useMemo(
    () =>
      districtId === ""
        ? []
        : Array.from(
            new Set(
              municipalBodies
                .filter(
                  (item) =>
                    item.district_id === Number(districtId) &&
                    item.is_active !== false,
                )
                .map((item) => item.body_type),
            ),
          ),
    [districtId, municipalBodies],
  );

  const filteredMunicipalBodies = useMemo(
    () =>
      districtId === "" || municipalBodyType === ""
        ? []
        : municipalBodies.filter(
            (item) =>
              item.district_id === Number(districtId) &&
              item.body_type === municipalBodyType &&
              item.is_active !== false,
          ),
    [districtId, municipalBodyType, municipalBodies],
  );

  const filteredWards = useMemo(
    () =>
      municipalBodyId === ""
        ? []
        : wards.filter(
            (item) =>
              item.municipal_body_id ===
                municipalBodyId &&
              item.is_active !== false,
          ),
    [municipalBodyId, wards],
  );

  useEffect(() => {
    setTehsilId("");
    setBlockId("");
    setGramPanchayatId("");
    setVillageId("");
      setMunicipalBodyType("");
      setMunicipalBodyId("");
      setWardId("");
      setMunicipalBodyType("");
      setMunicipalBodyId("");
      setWardId("");
  }, [districtId]);

  useEffect(() => {
    setBlockId("");
    setGramPanchayatId("");
    setVillageId("");
  }, [tehsilId]);

  useEffect(() => {
    setGramPanchayatId("");
    setVillageId("");
  }, [blockId]);

  useEffect(() => {
    setWardId("");
  }, [municipalBodyId]);

  useEffect(() => {
  }, [wardId]);

  useEffect(() => {
    if (areaType === "rural") {
      setMunicipalBodyId("");
      setWardId("");
    } else {
      setTehsilId("");
      setBlockId("");
      setGramPanchayatId("");
      setVillageId("");
    }
  }, [areaType]);

  const resetRegistrationFields = () => {
    setFullName("");
    setEmail("");
    setMobile("");
    setFatherName("");
    setMotherName("");
    setGender("");
    setDob("");

    setAreaType("rural");
    setDistrictId("");
    setTehsilId("");
    setBlockId("");
    setGramPanchayatId("");
    setVillageId("");

    setMunicipalBodyId("");
    setWardId("");

    setAddress("");
    setPincode("");
  };

  const handleSendOtp = async () => {
    /*
     * Validate the complete registration form BEFORE sending OTP.
     * No OTP API request should be made when any required field is missing.
     */

    if (!fullName.trim()) {
      toast.error("Please enter your full name");
      return;
    }

    if (!email.trim()) {
      toast.error("Please enter your email");
      return;
    }

    if (!username.trim()) {
      toast.error("Please choose a username");
      return;
    }

    if (!password) {
      toast.error("Please create a password");
      return;
    }

    if (!/^[6-9]\d{9}$/.test(mobile.trim())) {
      toast.error("Enter a valid 10-digit mobile number");
      return;
    }

    if (districtId === "") {
      toast.error("Please select your district");
      return;
    }

    if (areaType === "rural") {
      if (tehsilId === "") {
        toast.error("Please select your tehsil");
        return;
      }

      if (blockId === "") {
        toast.error("Please select your block / area");
        return;
      }

      if (gramPanchayatId === "") {
        toast.error("Please select your Gram Panchayat");
        return;
      }

      if (villageId === "") {
        toast.error("Please select your village");
        return;
      }
    }

    if (areaType === "urban") {
      if (municipalBodyType === "") {
        toast.error("Please select your local body type");
        return;
      }

      if (municipalBodyId === "") {
        toast.error("Please select your municipal body");
        return;
      }

      if (wardId === "") {
        toast.error("Please select your ward");
        return;
      }
    }

    if (!address.trim()) {
      toast.error("Please enter your address");
      return;
    }

    if (!pincode.trim()) {
      toast.error("Please enter your 6-digit pincode");
      return;
    }

    if (!/^\d{6}$/.test(pincode.trim())) {
      toast.error("Enter a valid 6-digit pincode");
      return;
    }

    if (requestOtpMutation.isPending) {
      return;
    }

    if (!/^[6-9]\d{9}$/.test(mobile)) {
      toast.error(
        "Enter a valid 10-digit mobile number",
      );
      return;
    }

    try {
      const response =
        await requestOtpMutation.mutateAsync({
          full_name: fullName.trim(),
          username: username.trim(),
          email: email.trim(),
          mobile: mobile.trim(),
          password,

          father_name:
            fatherName.trim() || null,
          mother_name:
            motherName.trim() || null,
          gender: gender || null,
          dob: dob || null,

          address: address.trim(),
          pincode: pincode.trim() || null,

          state_id: 1,
          district_id: Number(districtId),

          area_type: areaType,

          tehsil_id:
            areaType === "rural"
              ? Number(tehsilId)
              : null,

          block_id:
            areaType === "rural"
              ? Number(blockId)
              : null,

          gram_panchayat_id:
            areaType === "rural"
              ? Number(gramPanchayatId)
              : null,

          village_id:
            areaType === "rural"
              ? Number(villageId)
              : null,

          municipal_body_id:
            areaType === "urban"
              ? Number(municipalBodyId)
              : null,

          ward_id:
            areaType === "urban"
              ? Number(wardId)
              : null,

          // Locality master data is not available yet.
          // Keep the field optional for citizen registration.
          locality_id: null,
        });

      setRegistrationId(
        response.registration_id,
      );

      setOtpSent(true);
      setOtp("");
      setMobileVerified(false);

      toast.success(
        "OTP sent to your mobile number",
      );
    } catch (error: any) {
      console.error(
        "SEND OTP ERROR:",
        error,
      );

      const detail =
        error?.response?.data?.detail ??
        error?.response?.data?.message ??
        error?.message ??
        "Unable to send OTP";

      toast.error(String(detail));
    }
  };

  const handleVerifyOtp = async () => {
    if (!registrationId) {
      toast.error(
        "Please request OTP first",
      );
      return;
    }

    if (!/^\d{6}$/.test(otp)) {
      toast.error(
        "Enter a valid 6-digit OTP",
      );
      return;
    }

    try {
      const response =
        await verifyOtpMutation.mutateAsync({
          registration_id: registrationId,
          otp: otp.trim(),
        });

      setMobileVerified(true);

      toast.success(
        response.message ||
          "Registration successful",
      );

      setOtp("");
      setOtpSent(false);
      setRegistrationId(null);

      resetRegistrationFields();

      setMode("signin");
    } catch (error: any) {
      console.error(
        "VERIFY OTP ERROR:",
        error,
      );

      const detail =
        error?.response?.data?.detail ??
        error?.response?.data?.message ??
        error?.message ??
        "Invalid or expired OTP";

      toast.error(String(detail));
    }
  };

  const getRecoveryError = (error: any) =>
    String(
      error?.response?.data?.detail ??
        error?.response?.data?.message ??
        error?.message ??
        "Something went wrong. Please try again.",
    );

  const openRecovery = (
    type: "password" | "username",
  ) => {
    setRecoveryMode(type);
    setRecoveryStep("identifier");
    setRecoveryIdentifier("");
    setRecoveryId(null);
    setRecoveryOtp("");
    setRecoveryNewPassword("");
    setRecoveryConfirmPassword("");
  };

  const closeRecovery = () => {
    setRecoveryMode(null);
    setRecoveryStep("identifier");
    setRecoveryIdentifier("");
    setRecoveryId(null);
    setRecoveryOtp("");
    setRecoveryNewPassword("");
    setRecoveryConfirmPassword("");
  };

  const handleRecoveryRequestOtp = async () => {
    const identifier = recoveryIdentifier.trim();

    if (!identifier) {
      toast.error(
        "Enter your username, email or mobile number.",
      );
      return;
    }

    try {
      const result =
        recoveryMode === "password"
          ? await requestPasswordResetMutation.mutateAsync(
              identifier,
            )
          : await requestUsernameRecoveryMutation.mutateAsync(
              identifier,
            );

      setRecoveryId(result.recovery_id);
      setRecoveryStep("otp");

      toast.success("OTP sent to your registered mobile.");
    } catch (error: any) {
      toast.error(getRecoveryError(error));
    }
  };

  const handleRecoveryVerifyOtp = async () => {
    if (!recoveryId) {
      toast.error("Recovery session not found.");
      return;
    }

    if (!/^\d{6}$/.test(recoveryOtp)) {
      toast.error("Enter the 6-digit OTP.");
      return;
    }

    try {
      if (recoveryMode === "password") {
        await verifyPasswordResetOtpMutation.mutateAsync({
          recoveryId,
          otp: recoveryOtp,
        });

        setRecoveryStep("reset");
        toast.success("OTP verified successfully.");
      } else {
        const result =
          await verifyUsernameRecoveryOtpMutation.mutateAsync({
            recoveryId,
            otp: recoveryOtp,
          });

        setRecoveryIdentifier(result.username);
        setRecoveryStep("success");

        toast.success("Username recovered successfully.");
      }
    } catch (error: any) {
      toast.error(getRecoveryError(error));
    }
  };

  const handleRecoveryResetPassword = async () => {
    if (!recoveryId) {
      toast.error("Recovery session not found.");
      return;
    }

    if (recoveryNewPassword.length < 8) {
      toast.error(
        "Password must contain at least 8 characters.",
      );
      return;
    }

    if (recoveryNewPassword !== recoveryConfirmPassword) {
      toast.error("Passwords do not match.");
      return;
    }

    try {
      await resetPasswordMutation.mutateAsync({
        recoveryId,
        newPassword: recoveryNewPassword,
      });

      setRecoveryStep("success");
      toast.success("Password reset successfully.");
    } catch (error: any) {
      toast.error(getRecoveryError(error));
    }
  };

  const recoveryBusy =
    requestPasswordResetMutation.isPending ||
    verifyPasswordResetOtpMutation.isPending ||
    resetPasswordMutation.isPending ||
    requestUsernameRecoveryMutation.isPending ||
    verifyUsernameRecoveryOtpMutation.isPending;

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (mode === "register" && otpSent) {
      await handleVerifyOtp();
      return;
    }

    if (mode === "signin") {
      if (!username.trim()) {
        toast.error("Username is required");
        return;
      }

      if (!password) {
        toast.error("Password is required");
        return;
      }

      try {
        const user =
          await loginMutation.mutateAsync({
            username: username.trim(),
            password,
          });

        if (user.role_id !== 9) {
          toast.error(
            "This account is not registered as a Citizen.",
          );
          return;
        }

        toast.success("Login successful");

        navigate("/citizen", {
          replace: true,
        });
      } catch (error: any) {
        const message =
          error?.response?.data?.detail ??
          "Invalid username or password";

        toast.error(message);
      }

      return;
    }

    if (!fullName.trim()) {
      toast.error("Full name is required");
      return;
    }

    if (!username.trim()) {
      toast.error("Username is required");
      return;
    }

    if (!email.trim()) {
      toast.error("Email is required");
      return;
    }

    if (!password) {
      toast.error("Password is required");
      return;
    }

    if (!/^[6-9]\d{9}$/.test(mobile)) {
      toast.error(
        "Enter a valid 10-digit mobile number",
      );
      return;
    }

    if (districtId === "") {
      toast.error("Select your district");
      return;
    }

    if (!address.trim()) {
      toast.error("Address is required");
      return;
    }

    if (
      pincode.trim() &&
      !/^[0-9]{6}$/.test(
        pincode.trim(),
      )
    ) {
      toast.error(
        "Enter a valid 6-digit pincode",
      );
      return;
    }

    if (areaType === "rural") {
      if (tehsilId === "") {
        toast.error("Select your tehsil");
        return;
      }

      if (blockId === "") {
        toast.error("Select your block");
        return;
      }

      if (gramPanchayatId === "") {
        toast.error(
          "Select your Gram Panchayat",
        );
        return;
      }

      if (villageId === "") {
        toast.error("Select your village");
        return;
      }
    }

    if (areaType === "urban") {
      if (municipalBodyId === "") {
        toast.error(
          "Select your municipal body",
        );
        return;
      }

      if (wardId === "") {
        toast.error("Select your ward");
        return;
      }
    }

    await handleSendOtp();
  };

  const isSubmitting =
    loginMutation.isPending ||
    requestOtpMutation.isPending ||
    verifyOtpMutation.isPending;

  return (
    <div className="citizen-auth-page">

      <div className="citizen-auth-background">
        <div className="citizen-auth-image" />
        <div className="citizen-auth-image-overlay" />

        <div className="citizen-auth-orb citizen-auth-orb-one" />
        <div className="citizen-auth-orb citizen-auth-orb-two" />
        <div className="citizen-auth-orb citizen-auth-orb-three" />

        <div className="citizen-auth-grid" />
      </div>

      <header className="citizen-auth-header">
        <Link
          className="citizen-auth-brand"
          to="/login/citizen"
        >
          <div className="citizen-auth-brand-mark">
            <ShieldCheck size={25} />
          </div>

          <div className="citizen-auth-brand-text">
            <strong>UP_AI</strong>
            <small>
              Citizen Governance Platform
            </small>
          </div>
        </Link>

        <div className="citizen-auth-secure">
          <LockKeyhole size={14} />
          <span>
            Secure Citizen Access
          </span>
        </div>
      </header>

      <main className="citizen-auth-main">

        <section className="citizen-auth-intro">
          <div className="citizen-auth-eyebrow">
            <span />
            DIGITAL GOVERNANCE
          </div>

          <h1>
            Your voice.
            <br />
            <span>Your government.</span>
          </h1>

          <p>
            Access Uttar Pradesh citizen
            services, register complaints and
            stay connected with your government
            through UP_AI.
          </p>
        </section>

        <section className="citizen-auth-card-wrap">

          <div className="citizen-auth-card-glow" />

          <div className="citizen-auth-card">

            <div className="citizen-auth-card-header">
              <div className="citizen-auth-card-icon">
                <UserRound size={23} />
              </div>

              <div>
                <div className="citizen-auth-card-kicker">
                  CITIZEN PORTAL
                </div>

                <h2>
                  {mode === "register"
                    ? "Create your account"
                    : "Welcome back"}
                </h2>
              </div>
            </div>

            {!recoveryMode && (
              <div className="citizen-auth-switch">
                <button
                  type="button"
                  className={
                    mode === "signin"
                      ? "active"
                      : ""
                  }
                  onClick={() =>
                    setMode("signin")
                  }
                >
                  Sign In
                </button>

                <button
                  type="button"
                  className={
                    mode === "register"
                      ? "active"
                      : ""
                  }
                  onClick={() =>
                    setMode("register")
                  }
                >
                  Register
                </button>
              </div>
            )}


            {mode === "signin" && recoveryMode && (
              <section className="citizen-auth-recovery">

                <button
                  type="button"
                  className="citizen-auth-recovery-back"
                  onClick={closeRecovery}
                  disabled={recoveryBusy}
                >
                  ← Back to Sign In
                </button>

                <div className="citizen-auth-recovery-heading">
                  <div className="citizen-auth-recovery-icon">
                    {recoveryMode === "password" ? "🔐" : "👤"}
                  </div>

                  <div>
                    <div className="citizen-auth-card-kicker">
                      ACCOUNT RECOVERY
                    </div>

                    <h3>
                      {recoveryStep === "success"
                        ? recoveryMode === "password"
                          ? "Password updated"
                          : "Username recovered"
                        : recoveryMode === "password"
                          ? "Forgot your password?"
                          : "Forgot your username?"}
                    </h3>
                  </div>
                </div>

                {recoveryStep === "identifier" && (
                  <>
                    <p className="citizen-auth-recovery-text">
                      {recoveryMode === "password"
                        ? "Enter your registered username, email or mobile number. We will send a verification OTP."
                        : "Enter your registered email or mobile number. We will send a verification OTP."}
                    </p>

                    <label>
                      <span>
                        {recoveryMode === "password"
                          ? "Username / Email / Mobile"
                          : "Email / Mobile"}
                      </span>

                      <div className="citizen-auth-input">
                        <UserRound size={17} />

                        <input
                          value={recoveryIdentifier}
                          onChange={(event) =>
                            setRecoveryIdentifier(
                              event.target.value,
                            )
                          }
                          placeholder={
                            recoveryMode === "password"
                              ? "Enter your username, email or mobile"
                              : "Enter your email or mobile"
                          }
                          autoComplete="username"
                          disabled={recoveryBusy}
                        />
                      </div>
                    </label>

                    <button
                      type="button"
                      className="citizen-auth-submit"
                      onClick={handleRecoveryRequestOtp}
                      disabled={recoveryBusy}
                    >
                      <span>
                        {recoveryBusy
                          ? "Sending OTP..."
                          : "Send OTP"}
                      </span>
                      <ArrowRight size={18} />
                    </button>
                  </>
                )}

                {recoveryStep === "otp" && (
                  <>
                    <p className="citizen-auth-recovery-text">
                      Enter the 6-digit OTP sent to your registered mobile number.
                    </p>

                    <label>
                      <span>Verification OTP</span>

                      <div className="citizen-auth-input">
                        <ShieldCheck size={17} />

                        <input
                          value={recoveryOtp}
                          onChange={(event) =>
                            setRecoveryOtp(
                              event.target.value
                                .replace(/\D/g, "")
                                .slice(0, 6),
                            )
                          }
                          placeholder="Enter 6-digit OTP"
                          inputMode="numeric"
                          autoComplete="one-time-code"
                          disabled={recoveryBusy}
                        />
                      </div>
                    </label>

                    <button
                      type="button"
                      className="citizen-auth-submit"
                      onClick={handleRecoveryVerifyOtp}
                      disabled={
                        recoveryBusy ||
                        recoveryOtp.length !== 6
                      }
                    >
                      <span>
                        {recoveryBusy
                          ? "Verifying..."
                          : "Verify OTP"}
                      </span>
                      <ArrowRight size={18} />
                    </button>
                  </>
                )}

                {recoveryStep === "reset" && (
                  <>
                    <p className="citizen-auth-recovery-text">
                      Create a new password for your Citizen Portal account.
                    </p>

                    <label>
                      <span>New Password</span>

                      <div className="citizen-auth-input">
                        <LockKeyhole size={17} />

                        <input
                          type="password"
                          value={recoveryNewPassword}
                          onChange={(event) =>
                            setRecoveryNewPassword(
                              event.target.value,
                            )
                          }
                          placeholder="Enter new password"
                          autoComplete="new-password"
                          disabled={recoveryBusy}
                        />
                      </div>
                    </label>

                    <label>
                      <span>Confirm Password</span>

                      <div className="citizen-auth-input">
                        <LockKeyhole size={17} />

                        <input
                          type="password"
                          value={recoveryConfirmPassword}
                          onChange={(event) =>
                            setRecoveryConfirmPassword(
                              event.target.value,
                            )
                          }
                          placeholder="Confirm new password"
                          autoComplete="new-password"
                          disabled={recoveryBusy}
                        />
                      </div>
                    </label>

                    <button
                      type="button"
                      className="citizen-auth-submit"
                      onClick={handleRecoveryResetPassword}
                      disabled={recoveryBusy}
                    >
                      <span>
                        {recoveryBusy
                          ? "Updating Password..."
                          : "Update Password"}
                      </span>
                      <ArrowRight size={18} />
                    </button>
                  </>
                )}

                {recoveryStep === "success" && (
                  <div className="citizen-auth-recovery-success">
                    <div className="citizen-auth-recovery-success-icon">
                      ✓
                    </div>

                    <h4>
                      {recoveryMode === "password"
                        ? "Password reset successful"
                        : "Your username is"}
                    </h4>

                    {recoveryMode === "username" && (
                      <div className="citizen-auth-recovered-username">
                        {recoveryIdentifier}
                      </div>
                    )}

                    <p>
                      {recoveryMode === "password"
                        ? "Your password has been updated. You can now sign in with your new password."
                        : "Keep this username safe. You can now use it to sign in to the Citizen Portal."}
                    </p>

                    <button
                      type="button"
                      className="citizen-auth-submit"
                      onClick={() => {
                        closeRecovery();
                        setMode("signin");
                      }}
                    >
                      <span>Back to Sign In</span>
                      <ArrowRight size={18} />
                    </button>
                  </div>
                )}

              </section>
            )}

            <form
              className={
                (mode === "register"
                  ? "citizen-auth-form citizen-auth-register-form"
                  : "citizen-auth-form") +
                (recoveryMode ? " citizen-auth-form-hidden" : "")
              }
              onSubmit={handleSubmit}
            >

              {mode === "register" && (
                <>
                  <div className="citizen-auth-form-section-title">
                    Personal details
                  </div>

                  <label>
                    <span>Full Name</span>
                    <div className="citizen-auth-input">
                      <UserRound size={17} />
                      <input
                        value={fullName}
                        onChange={(event) =>
                          setFullName(
                            event.target.value,
                          )
                        }
                        placeholder="Enter your full name"
                        autoComplete="name"
                      />
                    </div>
                  </label>

                  <label>
                    <span>Email</span>
                    <div className="citizen-auth-input">
                      <input
                        value={email}
                        onChange={(event) =>
                          setEmail(
                            event.target.value,
                          )
                        }
                        placeholder="Enter your email"
                        type="email"
                        autoComplete="email"
                      />
                    </div>
                  </label>

                  <div className="citizen-auth-form-section-title">
                    Account details
                  </div>

                  <label>
                    <span>Username</span>

                    <div className="citizen-auth-input">
                      <UserRound size={17} />

                      <input
                        value={username}
                        onChange={(event) =>
                          setUsername(
                            event.target.value,
                          )
                        }
                        placeholder="Choose username"
                        autoComplete="username"
                        disabled={isSubmitting}
                      />
                    </div>
                  </label>

                  <label>
                    <span>Password</span>

                    <div className="citizen-auth-input">
                      <LockKeyhole size={17} />

                      <input
                        value={password}
                        onChange={(event) =>
                          setPassword(
                            event.target.value,
                          )
                        }
                        type={
                          showPassword
                            ? "text"
                            : "password"
                        }
                        placeholder="Create password"
                        autoComplete="new-password"
                        disabled={isSubmitting}
                      />

                      <button
                        type="button"
                        className="citizen-auth-eye"
                        onClick={() =>
                          setShowPassword(
                            (value) => !value,
                          )
                        }
                      >
                        {showPassword ? (
                          <EyeOff size={17} />
                        ) : (
                          <Eye size={17} />
                        )}
                      </button>
                    </div>
                  </label>

                  <div className="citizen-auth-form-section-title">
                    Location
                  </div>

<label>
                    <span>District</span>

                    <select
                      value={districtId}
                      onChange={(event) =>
                        setDistrictId(
                          event.target.value ===
                            ""
                            ? ""
                            : Number(
                                event.target.value,
                              ),
                        )
                      }
                      className="citizen-auth-select"
                    >
                      <option value="">
                        Select District
                      </option>

                      {districts.map(
                        (district) => (
                          <option
                            key={district.id}
                            value={district.id}
                          >
                            {district.district_name}
                          </option>
                        ),
                      )}
                    </select>
                  </label>



                  <div className="citizen-auth-area-switch">
                    <button
                      type="button"
                      className={
                        areaType === "rural"
                          ? "active"
                          : ""
                      }
                      onClick={() =>
                        setAreaType("rural")
                      }
                    >
                      Rural
                    </button>

                    <button
                      type="button"
                      className={
                        areaType === "urban"
                          ? "active"
                          : ""
                      }
                      onClick={() =>
                        setAreaType("urban")
                      }
                    >
                      Urban
                    </button>
                  </div>

                  {areaType === "rural" ? (
                    <>
                      <label>
                        <span>Tehsil</span>

                        <select
                          value={tehsilId}
                          onChange={(event) =>
                            setTehsilId(
                              event.target.value ===
                                ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  ),
                            )
                          }
                          disabled={
                            districtId === ""
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            Select Tehsil
                          </option>

                          {filteredTehsils.map(
                            (item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.tehsil_name}
                              </option>
                            ),
                          )}
                        </select>
                      </label>

                      <label>
                        <span>Block / Area</span>

                        <select
                          value={blockId}
                          onChange={(event) =>
                            setBlockId(
                              event.target.value ===
                                ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  ),
                            )
                          }
                          disabled={
                            tehsilId === ""
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            Select Block / Area
                          </option>

                          {filteredBlocks.map(
                            (item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.block_name}
                              </option>
                            ),
                          )}
                        </select>
                      </label>

                      <label>
                        <span>Gram Panchayat</span>

                        <select
                          value={gramPanchayatId}
                          onChange={(event) => {
                            const value =
                              event.target.value === ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  );

                            setGramPanchayatId(value);
                            setVillageId("");
                          }}
                          disabled={
                            blockId === "" ||
                            isGramPanchayatsLoading
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            {isGramPanchayatsLoading
                              ? "Loading Gram Panchayats..."
                              : "Select Gram Panchayat"}
                          </option>

                          {gramPanchayats
                            .filter(
                              (item) =>
                                item.is_active !== false,
                            )
                            .map((item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.gram_panchayat_name}
                              </option>
                            ))}
                        </select>
                      </label>

                      <label>
                        <span>Village</span>

                        <select
                          value={villageId}
                          onChange={(event) =>
                            setVillageId(
                              event.target.value === ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  ),
                            )
                          }
                          disabled={
                            gramPanchayatId === "" ||
                            isVillagesLoading
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            {isVillagesLoading
                              ? "Loading Villages..."
                              : "Select Village"}
                          </option>

                          {villages
                            .filter(
                              (item) =>
                                item.is_active !== false,
                            )
                            .map((item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.village_name}
                              </option>
                            ))}
                        </select>
                      </label>
                    </>
                  ) : (
                    <>
                      <label>
                        <span>Local Body Type</span>

                        <select
                          value={municipalBodyType}
                          onChange={(event) =>
                            setMunicipalBodyType(
                              event.target.value as
                                | ""
                                | "NAGAR_NIGAM"
                                | "NAGAR_PALIKA_PARISHAD"
                                | "NAGAR_PANCHAYAT"
                                | "NOTIFIED_AREA_COUNCIL"
                                | "CANTONMENT_BOARD",
                            )
                          }
                          disabled={districtId === ""}
                          className="citizen-auth-select"
                        >
                          <option value="">
                            Select Local Body Type
                          </option>

                          {availableMunicipalBodyTypes.includes("NAGAR_NIGAM") && (
                            <option value="NAGAR_NIGAM">
                              Nagar Nigam
                            </option>
                          )}

                          {availableMunicipalBodyTypes.includes("NAGAR_PALIKA_PARISHAD") && (
                            <option value="NAGAR_PALIKA_PARISHAD">
                              Nagar Palika Parishad
                            </option>
                          )}

                          {availableMunicipalBodyTypes.includes("NAGAR_PANCHAYAT") && (
                            <option value="NAGAR_PANCHAYAT">
                              Nagar Panchayat
                            </option>
                          )}

                          {availableMunicipalBodyTypes.includes("NOTIFIED_AREA_COUNCIL") && (
                            <option value="NOTIFIED_AREA_COUNCIL">
                              Notified Area Council
                            </option>
                          )}

                          {availableMunicipalBodyTypes.includes("CANTONMENT_BOARD") && (
                            <option value="CANTONMENT_BOARD">
                              Cantonment Board
                            </option>
                          )}
                        </select>
                      </label>

                      <label>
                        <span>
                          Municipal Body
                        </span>

                        <select
                          value={municipalBodyId}
                          onChange={(event) =>
                            setMunicipalBodyId(
                              event.target.value ===
                                ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  ),
                            )
                          }
                          disabled={
                            districtId === "" ||
                            municipalBodyType === ""
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            Select Municipal Body
                          </option>

                          {filteredMunicipalBodies.map(
                            (item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.body_name}
                              </option>
                            ),
                          )}
                        </select>
                      </label>

                      <label>
                        <span>Ward</span>

                        <select
                          value={wardId}
                          onChange={(event) =>
                            setWardId(
                              event.target.value ===
                                ""
                                ? ""
                                : Number(
                                    event.target.value,
                                  ),
                            )
                          }
                          disabled={
                            municipalBodyId === ""
                          }
                          className="citizen-auth-select"
                        >
                          <option value="">
                            Select Ward
                          </option>

                          {filteredWards.map(
                            (item) => (
                              <option
                                key={item.id}
                                value={item.id}
                              >
                                {item.ward_name}
                              </option>
                            ),
                          )}
                        </select>
                      </label>

                    </>
                  )}

                  <label>
                    <span>Address</span>

                    <div className="citizen-auth-input">
                      <MapPin size={17} />

                      <input
                        value={address}
                        onChange={(event) =>
                          setAddress(
                            event.target.value,
                          )
                        }
                        placeholder="House / village / locality address"
                        autoComplete="street-address"
                      />
                    </div>
                  </label>

                  <label>
                    <span>Pincode</span>

                    <div className="citizen-auth-input">
                      <input
                        value={pincode}
                        onChange={(event) =>
                          setPincode(
                            event.target.value
                              .replace(
                                /\D/g,
                                "",
                              )
                              .slice(0, 6),
                          )
                        }
                        placeholder="6-digit pincode"
                        inputMode="numeric"
                      />
                    </div>
                  </label>

                  <label className="citizen-auth-mobile-field">
                    <span>Mobile Number</span>

                    <div className="citizen-auth-mobile-row">
                      <div className="citizen-auth-input">
                        <input
                          value={mobile}
                          onChange={(event) => {
                            const value =
                              event.target.value
                                .replace(
                                  /\D/g,
                                  "",
                                )
                                .slice(0, 10);

                            setMobile(value);

                            if (
                              mobileVerified
                            ) {
                              setMobileVerified(
                                false,
                              );
                              setOtpSent(false);
                              setOtp("");
                              setRegistrationId(
                                null,
                              );
                            }
                          }}
                          placeholder="10-digit mobile number"
                          inputMode="numeric"
                          autoComplete="tel"
                          disabled={
                            requestOtpMutation.isPending ||
                            verifyOtpMutation.isPending
                          }
                        />
                      </div>

                      <button
                        type="button"
                        className="citizen-auth-otp-button"
                        onClick={() => {
                          void handleSendOtp();
                        }}
                        disabled={
                          requestOtpMutation.isPending ||
                          verifyOtpMutation.isPending ||
                          mobile.length !== 10
                        }
                      >
                        {requestOtpMutation.isPending
                          ? "Sending..."
                          : otpSent
                            ? "Resend OTP"
                            : "Send OTP"}
                      </button>
                    </div>
                  </label>

                  {otpSent && (
                    <div className="citizen-auth-otp-section citizen-auth-otp-field">
                      <label>
                        <span>Enter OTP</span>

                        <div className="citizen-auth-otp-row">
                          <div className="citizen-auth-input">
                            <input
                              value={otp}
                              onChange={(event) =>
                                setOtp(
                                  event.target.value
                                    .replace(/\D/g, "")
                                    .slice(0, 6),
                                )
                              }
                              placeholder="6-digit OTP"
                              inputMode="numeric"
                              autoComplete="one-time-code"
                              maxLength={6}
                            />
                          </div>

                          <button
                            type="button"
                            className="citizen-auth-otp-button"
                            onClick={() => {
                              void handleVerifyOtp();
                            }}
                            disabled={
                              verifyOtpMutation.isPending ||
                              otp.length !== 6
                            }
                          >
                            {verifyOtpMutation.isPending
                              ? "Verifying..."
                              : "Verify OTP"}
                          </button>
                        </div>
                      </label>

                      <div className="citizen-auth-otp-meta">
                        <span>
                          OTP sent to ******{mobile.slice(-4)}
                        </span>

                        <span>
                          Enter the OTP received on your mobile.
                        </span>
                      </div>
                    </div>
                  )}

                  {mobileVerified && (
                    <div className="citizen-auth-mobile-verified">
                      ✓ Mobile number verified
                    </div>
                  )}

                </>
              )}

              {mode === "signin" && (
                <>
                  <label>
                    <span>Username</span>

                    <div className="citizen-auth-input">
                      <UserRound size={17} />

                      <input
                        value={username}
                        onChange={(event) =>
                          setUsername(
                            event.target.value,
                          )
                        }
                        placeholder="Enter your username"
                        autoComplete="username"
                        disabled={isSubmitting}
                      />
                    </div>
                  </label>

                  <label>
                    <span>Password</span>

                    <div className="citizen-auth-input">
                      <LockKeyhole size={17} />

                      <input
                        value={password}
                        onChange={(event) =>
                          setPassword(
                            event.target.value,
                          )
                        }
                        type={
                          showPassword
                            ? "text"
                            : "password"
                        }
                        placeholder="Enter your password"
                        autoComplete="current-password"
                        disabled={isSubmitting}
                      />

                      <button
                        type="button"
                        className="citizen-auth-eye"
                        onClick={() =>
                          setShowPassword(
                            (value) => !value,
                          )
                        }
                      >
                        {showPassword ? (
                          <EyeOff size={17} />
                        ) : (
                          <Eye size={17} />
                        )}
                      </button>
                    </div>
                  </label>

                  <div className="citizen-auth-forgot-row">
                    <button
                      type="button"
                      onClick={() =>
                        openRecovery("password")
                      }
                    >
                      Forgot password?
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        openRecovery("username")
                      }
                    >
                      Forgot username?
                    </button>
                  </div>
                </>
              )}

              {!recoveryMode && mode === "signin" && (
              <button
                className="citizen-auth-submit"
                type="submit"
                disabled={isSubmitting}
              >
                <span>
                  {loginMutation.isPending
                    ? "Signing in..."
                    : "Sign in to Citizen Portal"}
                </span>

                <ArrowRight size={18} />
              </button>
              )}
            </form>

            <div className="citizen-auth-card-footer">
              <ShieldCheck size={15} />

              <span>
                Your information is protected by secure
                authentication.
              </span>
            </div>
          </div>
        </section>
      </main>

      <footer className="citizen-auth-footer">
        <span>UP_AI</span>
        <span>
          Digital Governance Platform
        </span>
      </footer>
    </div>
  );
}
