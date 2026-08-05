import React, { useState, useEffect } from 'react';

export default function ClaimDashboard() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    // In production, this fetches from the FastAPI backend
    // fetch('/api/v1/claims').then(res => res.json()).then(setClaims)
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Claims Adjuster Portal</h1>
        <div className="space-x-4">
          <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-semibold">12 Flagged</span>
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">45 Auto-Approved</span>
        </div>
      </header>

      <main className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">Claim ID</th>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">Object / Part</th>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">Issue</th>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">AI Status</th>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">Risk Flags</th>
              <th className="px-6 py-4 text-sm font-medium text-gray-500">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {/* Example Row */}
            <tr className="hover:bg-gray-50 transition">
              <td className="px-6 py-4 text-sm text-gray-900 font-medium">#CLM-001</td>
              <td className="px-6 py-4 text-sm text-gray-600">car / front_bumper</td>
              <td className="px-6 py-4 text-sm text-gray-600">crack (high)</td>
              <td className="px-6 py-4">
                <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-semibold">
                  Manual Review
                </span>
              </td>
              <td className="px-6 py-4">
                <span className="text-xs text-red-600 font-semibold border border-red-200 px-2 py-1 rounded">
                  vehicle_identity_mismatch
                </span>
              </td>
              <td className="px-6 py-4">
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">Review</button>
              </td>
            </tr>
          </tbody>
        </table>
      </main>
    </div>
  );
}
