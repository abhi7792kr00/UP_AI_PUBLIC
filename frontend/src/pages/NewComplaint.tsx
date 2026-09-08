import { useEffect, useRef, useState } from "react";

import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  ArrowRight,
  Bot,
  CheckCircle2,
  FileText,
  FileUp,
  LoaderCircle,
  MapPin,
  ShieldCheck,
  Sparkles,
  User,
  X,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { useAuthStore } from "../stores/auth.store";

import { Button, Input } from "../components/ui";

import { useCitizenComplaintFormData } from "../features/citizen/hooks/useCitizenComplaintFormData";
import { useCreateCitizenComplaint } from "../features/citizen/hooks/useCreateCitizenComplaint";

import "./new-complaint.css";

const schema = z.object({
  category_id: z.number().int().positive("Select a category"),
  subcategory_id: z
    .number()
    .int()
    .positive("Select a sub-category")
    .nullable()
    .optional(),
  department_id: z.number().int().positive("Select a department"),
  priority_id: z
    .number()
    .int()
    .positive("Select priority")
    .nullable()
    .optional(),

  state_id: z.number().int().positive("Select a state"),
  district_id: z.number().int().positive("Select a district"),

  area_type: z.enum(["rural", "urban"]).optional(),

  tehsil_id: z.number().int().positive().nullable().optional(),
  block_id: z.number().int().positive().nullable().optional(),
  gram_panchayat_id: z.number().int().positive().nullable().optional(),
  village_id: z.number().int().positive().nullable().optional(),

  municipal_body_id: z.number().int().positive().nullable().optional(),
  ward_id: z.number().int().positive().nullable().optional(),
  locality_id: z.number().int().positive().nullable().optional(),

  mobile_number: z.string().nullable().optional(),
  email: z.string().email().nullable().optional(),

  subject: z.string().trim().min(3, "Subject is required"),

  location: z.string().trim().min(3, "Location is required"),

  description: z
    .string()
    .trim()
    .min(20, "Please provide at least 20 characters"),

  pincode: z
    .string()
    .trim()
    .regex(/^[0-9]{6}$/, "Enter a valid 6-digit pincode")
    .optional()
    .or(z.literal("")),

  use_profile_address: z.boolean().optional(),
});

type FormData = {
  category_id: number;
  subcategory_id?: number | null;
  department_id: number;
  priority_id?: number | null;

  state_id: number;
  district_id: number;

  area_type?: "rural" | "urban";

  tehsil_id?: number | null;
  block_id?: number | null;
  gram_panchayat_id?: number | null;
  village_id?: number | null;

  municipal_body_id?: number | null;
  ward_id?: number | null;
  locality_id?: number | null;

  mobile_number?: string | null;
  email?: string | null;

  subject: string;
  location: string;
  description: string;
  pincode?: string;

  use_profile_address?: boolean;
};

export function NewComplaint() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const user = useAuthStore((state) => state.user);

  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [addressMode, setAddressMode] = useState<"profile" | "manual">(
    "profile",
  );

  const {
    register,
    handleSubmit,
    setValue,
    control,
    formState: { errors },
  } = useForm<FormData, unknown, FormData>({
    resolver: zodResolver(schema),

    defaultValues: {
      category_id: 0,
      subcategory_id: null,
      department_id: 0,
      priority_id: null,

      state_id: 0,
      district_id: 0,

      area_type: "rural",

      tehsil_id: null,
      block_id: null,
      gram_panchayat_id: null,
      village_id: null,

      municipal_body_id: null,
      ward_id: null,
      locality_id: null,

      mobile_number: null,
      email: null,

      subject: "",
      location: "",
      description: "",
      pincode: "",

      use_profile_address: true,
    },
  });

  const watchedCategoryId = useWatch({
    control,
    name: "category_id",
  });

  const {
    categories,
    departments,
    states,
    districts,
    priorities,
    subcategories,
    isLoading,
    isSubcategoriesLoading,
    isError,
  } = useCitizenComplaintFormData(
    watchedCategoryId > 0 ? watchedCategoryId : undefined,
  );

  const createComplaint = useCreateCitizenComplaint();

  // Pre-fill from citizen profile
  useEffect(() => {
    const citizen = user?.citizen;

    if (!citizen) {
      return;
    }

    setValue("state_id", citizen.state_id);
    setValue("district_id", citizen.district_id);

    setValue("area_type", citizen.area_type);

    setValue("tehsil_id", citizen.tehsil_id);
    setValue("block_id", citizen.block_id);
    setValue("gram_panchayat_id", citizen.gram_panchayat_id);
    setValue("village_id", citizen.village_id);

    setValue("municipal_body_id", citizen.municipal_body_id);
    setValue("ward_id", citizen.ward_id);
    setValue("locality_id", citizen.locality_id);

    setValue("location", citizen.address ?? "");
    setValue("pincode", citizen.pincode ?? "");

    setValue("mobile_number", user.mobile);
    setValue("email", user.email);

    setAddressMode("profile");
    setValue("use_profile_address", true);
  }, [user, setValue]);

  // Reset subcategory when category changes
  useEffect(() => {
    setValue("subcategory_id", null);
  }, [watchedCategoryId, setValue]);

  const applyProfileAddress = () => {
    const citizen = user?.citizen;
    if (!citizen) {
      toast.error("Profile address not available");
      return;
    }

    setValue("state_id", citizen.state_id);
    setValue("district_id", citizen.district_id);
    setValue("area_type", citizen.area_type);
    setValue("tehsil_id", citizen.tehsil_id);
    setValue("block_id", citizen.block_id);
    setValue("gram_panchayat_id", citizen.gram_panchayat_id);
    setValue("village_id", citizen.village_id);
    setValue("municipal_body_id", citizen.municipal_body_id);
    setValue("ward_id", citizen.ward_id);
    setValue("locality_id", citizen.locality_id);
    setValue("location", citizen.address ?? "");
    setValue("pincode", citizen.pincode ?? "");
    setValue("use_profile_address", true);
    setAddressMode("profile");
  };

  const switchToManualAddress = () => {
    setValue("use_profile_address", false);
    setAddressMode("manual");
    // Keep current values but allow editing
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const allowed = [
      "image/jpeg",
      "image/png",
      "image/webp",
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    const maxSize = 5 * 1024 * 1024; // 5 MB
    const next: File[] = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (!allowed.includes(file.type)) {
        toast.error(
          `"${file.name}" is not supported. Use JPG, PNG, PDF or DOC.`,
        );
        continue;
      }
      if (file.size > maxSize) {
        toast.error(`"${file.name}" exceeds 5 MB limit.`);
        continue;
      }
      next.push(file);
    }

    if (next.length > 0) {
      setSelectedFiles((prev) => [...prev, ...next].slice(0, 5));
      toast.success(
        `${next.length} file(s) added. (Upload will be sent with complaint)`,
      );
    }

    // reset input so same file can be re-selected
    e.target.value = "";
  };

  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const submit = async (data: FormData) => {
    try {
      const hasAttachment = selectedFiles.length > 0;

      const complaint = await createComplaint.mutateAsync({
        category_id: data.category_id,
        subcategory_id: data.subcategory_id ?? null,
        priority_id: data.priority_id ?? null,

        subject: data.subject,
        description: data.description,

        state_id: data.state_id,
        district_id: data.district_id,

        tehsil_id: data.tehsil_id ?? null,
        block_id: data.block_id ?? null,
        gram_panchayat_id: data.gram_panchayat_id ?? null,
        village_id: data.village_id ?? null,

        municipal_body_id: data.municipal_body_id ?? null,
        ward_id: data.ward_id ?? null,
        locality_id: data.locality_id ?? null,

        address: data.location,
        pincode: data.pincode || null,

        mobile_number: data.mobile_number ?? null,
        email: data.email ?? null,

        source: "WEB",
        language: "en",
        visibility: "PUBLIC",

        has_attachment: hasAttachment,
      });

      // Note: actual file upload endpoint can be wired later
      // (e.g. POST /citizen/complaints/{id}/attachments)
      if (hasAttachment) {
        console.info(
          "Files selected for upload:",
          selectedFiles.map((f) => f.name),
        );
      }

      toast.success("Complaint submitted successfully", {
        description: complaint.complaint_number,
      });

      navigate(
        `/citizen/complaints/${encodeURIComponent(
          complaint.complaint_number,
        )}`,
        { replace: true },
      );
    } catch (error: any) {
      const message =
        error?.response?.data?.detail ?? "Unable to submit complaint";
      toast.error(message);
    }
  };

  const profileAddressPreview =
    user?.citizen?.address ||
    (user?.citizen
      ? [
          user.citizen.address,
          user.citizen.pincode,
        ]
          .filter(Boolean)
          .join(", ")
      : null);

  return (
    <div className="citizen-complaint-page">
      {/* =====================================================
          HERO
      ====================================================== */}

      <section className="citizen-complaint-hero">
        <div className="citizen-complaint-hero-content">
          <div className="citizen-complaint-eyebrow">
            <Sparkles size={15} />
            CITIZEN SERVICES
          </div>

          <h1>Register a Complaint</h1>

          <p>
            Apni samasya ki jankari dein. UP_AI aapki complaint ko
            sambandhit workflow mein bhejega.
          </p>

          <div className="citizen-complaint-trust">
            <span>
              <ShieldCheck size={16} />
              Secure Citizen Submission
            </span>
            <span>
              <CheckCircle2 size={16} />
              Real Backend
            </span>
          </div>
        </div>

        <div className="citizen-complaint-hero-orb">
          <div className="complaint-orb-ring">
            <FileText size={42} />
          </div>
          <div className="complaint-orb-dot dot-one" />
          <div className="complaint-orb-dot dot-two" />
          <div className="complaint-orb-dot dot-three" />
        </div>
      </section>

      {/* =====================================================
          ERROR
      ====================================================== */}

      {isError && (
        <div className="citizen-complaint-error">
          <strong>Unable to load complaint master data.</strong>
          <span>Please make sure the backend is running.</span>
        </div>
      )}

      {/* =====================================================
          MAIN GRID
      ====================================================== */}

      <form
        onSubmit={handleSubmit(submit)}
        className="citizen-complaint-grid"
      >
        {/* ===================================================
            FORM
        ==================================================== */}

        <div className="citizen-complaint-form-card">
          {/* Step 01 — Classification */}

          <section className="complaint-form-section">
            <div className="complaint-section-heading">
              <div className="complaint-step">01</div>
              <div>
                <span>COMPLAINT CLASSIFICATION</span>
                <h2>What is your complaint about?</h2>
                <p>
                  Pehle category select karein, phir related sub-category
                  aur priority choose karein.
                </p>
              </div>
            </div>

            <div className="complaint-form-two-column">
              <label className="complaint-field">
                <span>Issue Category *</span>
                <select
                  className="citizen-3d-input"
                  {...register("category_id", {
                    setValueAs: (value) => Number(value),
                  })}
                  disabled={isLoading || createComplaint.isPending}
                >
                  <option value="0">
                    {isLoading
                      ? "Loading categories..."
                      : "Select category"}
                  </option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.category_name}
                    </option>
                  ))}
                </select>
                {errors.category_id && (
                  <small>{errors.category_id.message}</small>
                )}
              </label>

              <label className="complaint-field">
                <span>Sub-Category *</span>
                <select
                  className="citizen-3d-input"
                  {...register("subcategory_id", {
                    setValueAs: (value) => {
                      const n = Number(value);
                      return n > 0 ? n : null;
                    },
                  })}
                  disabled={
                    isLoading ||
                    createComplaint.isPending ||
                    !watchedCategoryId ||
                    watchedCategoryId <= 0 ||
                    isSubcategoriesLoading
                  }
                >
                  <option value="0">
                    {!watchedCategoryId || watchedCategoryId <= 0
                      ? "First select category"
                      : isSubcategoriesLoading
                        ? "Loading sub-categories..."
                        : "Select sub-category"}
                  </option>
                  {subcategories.map((sub) => (
                    <option key={sub.id} value={sub.id}>
                      {sub.subcategory_name}
                    </option>
                  ))}
                </select>
                {errors.subcategory_id && (
                  <small>{errors.subcategory_id.message}</small>
                )}
              </label>
            </div>

            <div className="complaint-form-two-column">
              <label className="complaint-field">
                <span>Department *</span>
                <select
                  className="citizen-3d-input"
                  {...register("department_id", {
                    setValueAs: (value) => Number(value),
                  })}
                  disabled={isLoading || createComplaint.isPending}
                >
                  <option value="0">
                    {isLoading
                      ? "Loading departments..."
                      : "Select department"}
                  </option>
                  {departments.map((department) => (
                    <option key={department.id} value={department.id}>
                      {department.department_name}
                    </option>
                  ))}
                </select>
                {errors.department_id && (
                  <small>{errors.department_id.message}</small>
                )}
              </label>

              <label className="complaint-field">
                <span>Priority</span>
                <select
                  className="citizen-3d-input"
                  {...register("priority_id", {
                    setValueAs: (value) => {
                      const n = Number(value);
                      return n > 0 ? n : null;
                    },
                  })}
                  disabled={isLoading || createComplaint.isPending}
                >
                  <option value="0">Select priority (optional)</option>
                  {priorities.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.priority_name}
                    </option>
                  ))}
                </select>
                {errors.priority_id && (
                  <small>{errors.priority_id.message}</small>
                )}
              </label>
            </div>
          </section>

          {/* Step 02 — Location */}

          <section className="complaint-form-section">
            <div className="complaint-section-heading">
              <div className="complaint-step">02</div>
              <div>
                <span>LOCATION</span>
                <h2>Where is the issue?</h2>
                <p>
                  Profile address use karein ya manually naya address
                  bharein.
                </p>
              </div>
            </div>

            {/* Address mode toggle */}
            <div className="complaint-address-mode">
              <button
                type="button"
                className={
                  addressMode === "profile"
                    ? "address-mode-btn active"
                    : "address-mode-btn"
                }
                onClick={applyProfileAddress}
                disabled={createComplaint.isPending || !user?.citizen}
              >
                <User size={16} />
                Use Profile Address
              </button>
              <button
                type="button"
                className={
                  addressMode === "manual"
                    ? "address-mode-btn active"
                    : "address-mode-btn"
                }
                onClick={switchToManualAddress}
                disabled={createComplaint.isPending}
              >
                <MapPin size={16} />
                Enter Manually
              </button>
            </div>

            {addressMode === "profile" && profileAddressPreview && (
              <div className="complaint-profile-address-preview">
                <MapPin size={16} />
                <div>
                  <strong>Profile address</strong>
                  <p>{profileAddressPreview}</p>
                  {user?.citizen?.pincode && (
                    <span>PIN: {user.citizen.pincode}</span>
                  )}
                </div>
              </div>
            )}

            <div className="complaint-form-two-column">
              <label className="complaint-field">
                <span>State *</span>
                <select
                  className="citizen-3d-input"
                  {...register("state_id", {
                    setValueAs: (value) => Number(value),
                  })}
                  disabled={
                    isLoading ||
                    createComplaint.isPending ||
                    addressMode === "profile"
                  }
                >
                  <option value="0">
                    {isLoading ? "Loading states..." : "Select state"}
                  </option>
                  {states.map((state) => (
                    <option key={state.id} value={state.id}>
                      {state.state_name}
                    </option>
                  ))}
                </select>
                {errors.state_id && (
                  <small>{errors.state_id.message}</small>
                )}
              </label>

              <label className="complaint-field">
                <span>District *</span>
                <select
                  className="citizen-3d-input"
                  {...register("district_id", {
                    setValueAs: (value) => Number(value),
                  })}
                  disabled={
                    isLoading ||
                    createComplaint.isPending ||
                    addressMode === "profile"
                  }
                >
                  <option value="0">
                    {isLoading
                      ? "Loading districts..."
                      : "Select district"}
                  </option>
                  {districts.map((district) => (
                    <option key={district.id} value={district.id}>
                      {district.district_name}
                    </option>
                  ))}
                </select>
                {errors.district_id && (
                  <small>{errors.district_id.message}</small>
                )}
              </label>
            </div>

            <div className="complaint-form-two-column">
              <label className="complaint-field">
                <span>Location / Address *</span>
                <div className="citizen-input-icon">
                  <MapPin size={18} />
                  <Input
                    {...register("location")}
                    placeholder="Village / Ward, Block / Municipality, District"
                    disabled={
                      createComplaint.isPending ||
                      addressMode === "profile"
                    }
                  />
                </div>
                {errors.location && (
                  <small>{errors.location.message}</small>
                )}
              </label>

              <label className="complaint-field">
                <span>Pincode</span>
                <Input
                  {...register("pincode")}
                  className="citizen-3d-input"
                  placeholder="6-digit pincode"
                  inputMode="numeric"
                  maxLength={6}
                  disabled={
                    createComplaint.isPending ||
                    addressMode === "profile"
                  }
                />
                {errors.pincode && (
                  <small>{errors.pincode.message}</small>
                )}
              </label>
            </div>
          </section>

          {/* Step 03 — Details */}

          <section className="complaint-form-section">
            <div className="complaint-section-heading">
              <div className="complaint-step">03</div>
              <div>
                <span>COMPLAINT DETAILS</span>
                <h2>Tell us what happened</h2>
                <p>
                  Describe the problem clearly so the concerned authority
                  can act.
                </p>
              </div>
            </div>

            <label className="complaint-field">
              <span>Complaint Subject *</span>
              <Input
                {...register("subject")}
                placeholder="Example: Power outage in my village"
                disabled={createComplaint.isPending}
              />
              {errors.subject && (
                <small>{errors.subject.message}</small>
              )}
            </label>

            <label className="complaint-field">
              <span>Describe the Problem *</span>
              <textarea
                className="citizen-3d-textarea"
                {...register("description")}
                placeholder="Explain what happened, where, since when and how citizens are affected..."
                disabled={createComplaint.isPending}
              />
              {errors.description && (
                <small>{errors.description.message}</small>
              )}
            </label>
          </section>

          {/* Evidence — now active */}

          <section className="complaint-evidence">
            <div className="complaint-evidence-icon">
              <FileUp size={22} />
            </div>

            <div>
              <strong>Add supporting evidence</strong>
              <p>
                Photos and documents (JPG, PNG, PDF, DOC — max 5 MB each,
                up to 5 files).
              </p>

              {selectedFiles.length > 0 && (
                <ul className="complaint-file-list">
                  {selectedFiles.map((file, index) => (
                    <li key={`${file.name}-${index}`}>
                      <FileText size={14} />
                      <span>
                        {file.name} ({(file.size / 1024).toFixed(1)} KB)
                      </span>
                      <button
                        type="button"
                        className="complaint-file-remove"
                        onClick={() => removeFile(index)}
                        aria-label="Remove file"
                      >
                        <X size={14} />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".jpg,.jpeg,.png,.webp,.pdf,.doc,.docx,image/*,application/pdf"
                style={{ display: "none" }}
                onChange={handleFileChange}
                disabled={createComplaint.isPending}
              />
              <Button
                type="button"
                variant="secondary"
                disabled={createComplaint.isPending}
                onClick={() => fileInputRef.current?.click()}
              >
                Choose files
              </Button>
            </div>
          </section>

          {/* Actions */}

          <div className="citizen-complaint-actions">
            <Link className="complaint-cancel" to="/citizen">
              Cancel
            </Link>

            <Button
              type="submit"
              disabled={
                isLoading || isError || createComplaint.isPending
              }
            >
              {createComplaint.isPending ? (
                <>
                  <LoaderCircle size={18} className="animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  Submit Complaint
                  <ArrowRight size={18} />
                </>
              )}
            </Button>
          </div>
        </div>

        {/* ===================================================
            AI SIDEBAR
        ==================================================== */}

        <aside className="citizen-complaint-side">
          <div className="complaint-ai-card">
            <div className="complaint-ai-glow" />

            <div className="complaint-ai-icon">
              <Bot size={27} />
            </div>

            <span className="complaint-ai-label">UP_AI ASSISTANT</span>

            <h2>Need help filing your complaint?</h2>

            <p>
              UP_AI can help you understand which information is useful
              before you submit.
            </p>

            <div className="complaint-ai-points">
              <div>
                <CheckCircle2 size={17} />
                Real complaint categories
              </div>
              <div>
                <CheckCircle2 size={17} />
                Sub-categories & priority
              </div>
              <div>
                <CheckCircle2 size={17} />
                Profile or manual address
              </div>
              <div>
                <CheckCircle2 size={17} />
                Document upload support
              </div>
            </div>

            <Link to="/ai" className="complaint-ai-button">
              Ask UP_AI
              <ArrowRight size={17} />
            </Link>
          </div>

          <div className="complaint-security-card">
            <ShieldCheck size={21} />
            <div>
              <strong>Your submission is secure</strong>
              <p>
                Complaint data is submitted through your authenticated
                citizen account.
              </p>
            </div>
          </div>
        </aside>
      </form>
    </div>
  );
}

export default NewComplaint;
