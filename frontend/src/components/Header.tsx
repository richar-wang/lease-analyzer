export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-4xl px-6 py-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Ontario Tenant Lease Analyzer
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Upload your lease to check for illegal or unenforceable clauses under
          the Residential Tenancies Act, 2006
        </p>
      </div>
    </header>
  );
}
