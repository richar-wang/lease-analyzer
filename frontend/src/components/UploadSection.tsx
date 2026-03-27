import { useCallback, useRef, useState } from "react";

export default function UploadSection({
  onFileSelected,
  onDemoClick,
  isLoading,
}: {
  onFileSelected: (file: File) => void;
  onDemoClick: () => void;
  isLoading: boolean;
}) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) onFileSelected(file);
    },
    [onFileSelected]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) onFileSelected(file);
    },
    [onFileSelected]
  );

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-12 text-center transition-colors ${
          isDragging
            ? "border-blue-400 bg-blue-50"
            : "border-gray-300 hover:border-gray-400 hover:bg-gray-50"
        } ${isLoading ? "pointer-events-none opacity-50" : ""}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
        />
        <div className="text-4xl mb-3">&#128196;</div>
        <p className="text-gray-700 font-medium">
          Drop your lease PDF here or click to browse
        </p>
        <p className="text-sm text-gray-500 mt-1">
          Supports text-based and scanned PDFs (max 10MB)
        </p>
      </div>

      <div className="text-center">
        <span className="text-sm text-gray-400">or</span>
      </div>

      <button
        onClick={onDemoClick}
        disabled={isLoading}
        className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
      >
        Try with a Demo Lease
      </button>
    </div>
  );
}
