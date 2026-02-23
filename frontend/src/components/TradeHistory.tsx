import React from 'react';

interface Trade {
    date: string;
    side: string;
    price: number;
    quantity: number;
}

interface TradeHistoryProps {
    trades: Trade[];
}

export function TradeHistory({ trades }: TradeHistoryProps) {
    return (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden backdrop-blur-sm">
            <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
                <h3 className="text-slate-200 font-semibold text-lg">Trade History</h3>
                <span className="text-xs text-slate-500 font-mono uppercase tracking-wider">{trades.length} Trades Executed</span>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left">
                    <thead>
                        <tr className="bg-slate-800/50 text-slate-400 text-xs uppercase tracking-wider">
                            <th className="px-6 py-3 font-medium">Time</th>
                            <th className="px-6 py-3 font-medium">Side</th>
                            <th className="px-6 py-3 font-medium">Price</th>
                            <th className="px-6 py-3 font-medium">Quantity</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {trades.map((trade, idx) => (
                            <tr key={idx} className="hover:bg-slate-800/30 transition-colors group">
                                <td className="px-6 py-4 text-sm text-slate-300 font-mono">{trade.date}</td>
                                <td className="px-6 py-4">
                                    <span className={`text-xs font-bold px-2 py-1 rounded ${trade.side === 'BUY' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                                        }`}>
                                        {trade.side}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-sm text-slate-100 font-medium">${trade.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                                <td className="px-6 py-4 text-sm text-slate-300 font-mono">{trade.quantity.toFixed(4)}</td>
                            </tr>
                        ))}
                        {trades.length === 0 && (
                            <tr>
                                <td colSpan={4} className="px-6 py-20 text-center text-slate-500 italic">No trades recorded for this period</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
