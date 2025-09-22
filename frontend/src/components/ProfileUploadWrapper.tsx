"use client";

import { useAuth } from '../contexts/AuthContext';
import ProfileUploadModal from './ProfileUploadModal';
import { useState, useEffect } from 'react';

interface ProfileUploadWrapperProps {
  children: React.ReactNode;
}

export default function ProfileUploadWrapper({ children }: ProfileUploadWrapperProps) {
  const { needsProfileUpload, setNeedsProfileUpload } = useAuth();
  const [showModal, setShowModal] = useState(false);

  // Show modal when user needs to upload profile
  useEffect(() => {
    if (needsProfileUpload) {
      setShowModal(true);
    }
  }, [needsProfileUpload]);

  const handleProfileUploaded = (profile: any) => {
    console.log("✅ Profile uploaded successfully:", profile);
    setNeedsProfileUpload(false);
    setShowModal(false);
    // The profile is already saved to database, the resume-writer page will auto-reload it
  };

  const handleCloseModal = () => {
    // Don't allow closing the modal if profile upload is required
    if (needsProfileUpload) {
      return;
    }
    setShowModal(false);
  };

  return (
    <>
      {children}
      <ProfileUploadModal
        isOpen={showModal || needsProfileUpload}
        onClose={handleCloseModal}
        onProfileUploaded={handleProfileUploaded}
      />
    </>
  );
}
