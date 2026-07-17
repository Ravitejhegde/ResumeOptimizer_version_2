import { useState } from "react";

import { uploadResume } from "../../services/resumeApi";

type Props = {
  onUploaded: (storedFilename: string) => void;
};

export default function UploadFeature({
  onUploaded,
}: Props) {
  const [loading, setLoading] = useState(false);

  async function handleChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    setLoading(true);

    try {
      const result = await uploadResume(file);

      onUploaded(
        result.data.stored_filename
      );
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input
        type="file"
        accept=".docx"
        onChange={handleChange}
      />

      {loading && <p>Uploading...</p>}
    </div>
  );
}