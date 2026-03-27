export default function LanguageToggle({
  isHebrew,
  onToggle,
}: {
  isHebrew: boolean;
  onToggle: () => void;
}) {
  return (
    <button
      onClick={onToggle}
      className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
        isHebrew
          ? "bg-[#0038A8] text-white hover:bg-[#002d8a]"
          : "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
      }`}
    >
      {isHebrew ? "Switch to English" : "עברית"}
    </button>
  );
}
