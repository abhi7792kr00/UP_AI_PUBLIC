import {
  MapPin,
  Mail,
  Phone,
  UserRound,
  ShieldCheck,
} from "lucide-react";

import { useCurrentUser } from "../../../features/auth/hooks/useCurrentUser";
import {
  useDistricts,
  useTehsils,
  useBlocks,
  useGramPanchayatsByBlock,
  useVillagesByGramPanchayat,
  useMunicipalBodies,
  useWards,
  useLocalities,
} from "../../../features/government/hooks/useGovernmentData";

import "./citizen-portal.css";

function valueOrDash(value: unknown) {
  return value === null || value === undefined || value === ""
    ? "—"
    : String(value);
}

export default function CitizenProfile() {
  const { data: user, isLoading } = useCurrentUser();

  const citizen = user?.citizen;

  const { data: districts } = useDistricts();
  const { data: tehsils } = useTehsils();
  const { data: blocks } = useBlocks();

  const { data: gramPanchayats } =
    useGramPanchayatsByBlock(citizen?.block_id ?? "");

  const { data: villages } =
    useVillagesByGramPanchayat(citizen?.gram_panchayat_id ?? "");

  const { data: municipalBodies } = useMunicipalBodies();
  const { data: wards } = useWards();
  const { data: localities } = useLocalities();

  if (isLoading) {
    return (
      <div className="citizen-portal-page">
        <div className="portal-empty">
          <h3>Loading profile...</h3>
          <p>Please wait while your profile is loaded.</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="citizen-portal-page">
        <div className="portal-empty">
          <h3>Profile unavailable</h3>
          <p>Unable to load your account information.</p>
        </div>
      </div>
    );
  }

  const districtName =
    districts?.find((item) => item.id === citizen?.district_id)
      ?.district_name;

  const tehsilName =
    tehsils?.find((item) => item.id === citizen?.tehsil_id)?.tehsil_name;

  const blockName =
    blocks?.find((item) => item.id === citizen?.block_id)?.block_name;

  const gramPanchayatName =
    gramPanchayats?.find(
      (item) => item.id === citizen?.gram_panchayat_id,
    )?.gram_panchayat_name;

  const villageName =
    villages?.find((item) => item.id === citizen?.village_id)?.village_name;

  const municipalBodyName =
    municipalBodies?.find(
      (item) => item.id === citizen?.municipal_body_id,
    )?.body_name;

  const wardName =
    wards?.find((item) => item.id === citizen?.ward_id)?.ward_name;

  const localityName =
    localities?.find(
      (item) => item.id === citizen?.locality_id,
    )?.locality_name;

  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">Citizen Account</div>
          <h1 className="portal-title">My Profile</h1>
          <p className="portal-description">
            View your registered account and address information.
          </p>
        </div>

        <div className="portal-grid">
          <section className="portal-card">
            <h2 className="portal-card-title">
              <UserRound size={19} />
              Personal Information
            </h2>

            <div className="portal-info-grid">
              <div className="portal-info-item">
                <span className="portal-info-label">Full Name</span>
                <span className="portal-info-value">
                  {valueOrDash(user.full_name)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Username</span>
                <span className="portal-info-value">
                  {valueOrDash(user.username)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Father's Name</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.father_name)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Mother's Name</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.mother_name)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Gender</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.gender)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Date of Birth</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.dob)}
                </span>
              </div>
            </div>
          </section>

          <section className="portal-card">
            <h2 className="portal-card-title">
              <Phone size={19} />
              Contact Information
            </h2>

            <div className="portal-info-grid">
              <div className="portal-info-item">
                <span className="portal-info-label">Mobile</span>
                <span className="portal-info-value">
                  {valueOrDash(user.mobile)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Email</span>
                <span className="portal-info-value">
                  {valueOrDash(user.email)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Account Status</span>
                <span className="portal-info-value">
                  {user.is_active ? "Active" : "Inactive"}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Citizen ID</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.id)}
                </span>
              </div>
            </div>
          </section>

          <section className="portal-card portal-card-full">
            <h2 className="portal-card-title">
              <MapPin size={19} />
              Registered Address
            </h2>

            <div className="portal-info-grid">
              <div className="portal-info-item">
                <span className="portal-info-label">Address</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.address)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Area Type</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.area_type)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">District</span>
                <span className="portal-info-value">
                  {valueOrDash(districtName ?? citizen?.district_id)}
                </span>
              </div>

              <div className="portal-info-item">
                <span className="portal-info-label">Tehsil</span>
                <span className="portal-info-value">
                  {valueOrDash(tehsilName ?? citizen?.tehsil_id)}
                </span>
              </div>

              {citizen?.area_type === "rural" ? (
                <>
                  <div className="portal-info-item">
                    <span className="portal-info-label">Block</span>
                    <span className="portal-info-value">
                      {valueOrDash(blockName ?? citizen.block_id)}
                    </span>
                  </div>

                  <div className="portal-info-item">
                    <span className="portal-info-label">Gram Panchayat</span>
                    <span className="portal-info-value">
                      {valueOrDash(
                        gramPanchayatName ?? citizen.gram_panchayat_id,
                      )}
                    </span>
                  </div>

                  <div className="portal-info-item">
                    <span className="portal-info-label">Village</span>
                    <span className="portal-info-value">
                      {valueOrDash(villageName ?? citizen.village_id)}
                    </span>
                  </div>
                </>
              ) : (
                <>
                  <div className="portal-info-item">
                    <span className="portal-info-label">
                      Municipal Body
                    </span>
                    <span className="portal-info-value">
                      {valueOrDash(
                        municipalBodyName ?? citizen?.municipal_body_id,
                      )}
                    </span>
                  </div>

                  <div className="portal-info-item">
                    <span className="portal-info-label">Ward</span>
                    <span className="portal-info-value">
                      {valueOrDash(wardName ?? citizen?.ward_id)}
                    </span>
                  </div>

                  <div className="portal-info-item">
                    <span className="portal-info-label">Locality</span>
                    <span className="portal-info-value">
                      {valueOrDash(localityName ?? citizen?.locality_id)}
                    </span>
                  </div>
                </>
              )}

              <div className="portal-info-item">
                <span className="portal-info-label">Pincode</span>
                <span className="portal-info-value">
                  {valueOrDash(citizen?.pincode)}
                </span>
              </div>
            </div>
          </section>

          <section className="portal-card portal-card-full">
            <h2 className="portal-card-title">
              <ShieldCheck size={19} />
              Account Security
            </h2>

            <p className="portal-description">
              Your account is protected through the authenticated UP_AI
              citizen portal.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}