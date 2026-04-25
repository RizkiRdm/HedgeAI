import React from 'react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-6 bg-slate-950 text-slate-50 font-mono">
      <h1 className="text-2xl font-bold mb-4 border-b border-slate-800 pb-2">CRYPTOHEDGE AI // LIVE_FEED</h1>
      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-8 bg-slate-900 border border-slate-800 p-4 h-[600px] overflow-y-auto">
          <p className="text-slate-500 italic">Connecting to websocket...</p>
        </div>
        <div className="col-span-4 flex flex-col gap-4">
          <div className="bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm text-slate-400 uppercase mb-2">Portfolio Snapshot</h2>
            <div className="text-3xl font-bold">$0.00</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm text-slate-400 uppercase mb-2">Ops Health</h2>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div className="bg-green-500 h-full w-[80%]"></div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
