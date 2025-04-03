// src/components/UploadForm.tsx
import React from "react";

interface UploadFormProps {
  label: string;
  accept?: string;
  onChange: (file: File | null) => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ label, accept, onChange }) => {
  return (
    <div style={{ marginBottom: "1rem" }}>
      <label>{label}: </label>
      <input
        type="file"
        accept={accept || ".pdf,.jpg,.jpeg,.png"}
        onChange={(e) => onChange(e.target.files?.[0] || null)}
      />
    </div>
  );
};

export default UploadForm;
