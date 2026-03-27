export default function Disclaimer({ isHebrew }: { isHebrew: boolean }) {
  const bg = isHebrew ? "bg-[#e8eef8] border-[#0038A8]/30 text-[#0038A8]" : "bg-amber-50 border-amber-200 text-amber-800";

  return (
    <div className={`border rounded-lg px-4 py-3 text-sm ${bg}`}>
      <strong>{isHebrew ? "הבהרה:" : "Disclaimer:"}</strong>{" "}
      {isHebrew
        ? "כלי זה מספק ניתוח מידעי בלבד ואינו מהווה ייעוץ משפטי. לייעוץ משפטי בנוגע לשכירות שלכם, פנו לעורך דין או פרלגל מורשה באונטריו."
        : "This tool provides informational analysis only and does not constitute legal advice. For legal advice regarding your tenancy, consult a licensed paralegal or lawyer in Ontario."}
    </div>
  );
}
