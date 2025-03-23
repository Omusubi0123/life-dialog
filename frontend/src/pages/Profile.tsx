import '../index.css';
import Footer from '../components/Footer';
import ProfileSection from '../components/ProfileSection';
import { useProfile } from '../hooks/useProfile';

export default function Profile() {
  const { profile, diaryLink, profileLink } = useProfile();

  return (
    <div className="bg-white">
      <ProfileSection profile={profile} />
      <Footer diaryLink={diaryLink} profileLink={profileLink} />
    </div>
  );
}
