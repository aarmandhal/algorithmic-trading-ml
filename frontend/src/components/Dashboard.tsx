'use client';

import React, { useState, useEffect } from 'react';
import {
    TrendingUp,
    BarChart3,
    ShieldAlert,
    Activity,
    Search,
    LayoutDashboard,
    Wallet,
    ArrowRightLeft
} from 'lucide-react';
import { StatCard } from './StatCard';
import { TradingChart } from './TradingChart';
import { TradeHistory } from './TradeHistory';

const API_BASE = 'http://localhost:8000';

export default function Dashboard() {
    const [ticker, setTicker] = useState('SPY');
    const [tickers, setTickers] = useState<string[]>([]);
    const [backtestData, setBacktestData] = useState<any>(null);
    const [stockData, setStockData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch(`${API_BASE}/tickers`)
            .then(res => res.json())
            .then(data => setTickers(data))
            .catch(err => console.error("Error fetching tickers:", err));
    }, []);

    const runAnalysis = async (selectedTicker: string) => {
        setLoading(true);
        setError(null);
        try {
            // 1. Fetch backtest
            const btRes = await fetch(`${API_BASE}/backtest/${selectedTicker}`);
            if (!btRes.ok) throw new Error("Failed to fetch backtest results");
            const btData = await btRes.json();
            setBacktestData(btData);

            // 2. Fetch raw price data for candlesticks
            const priceRes = await fetch(`${API_BASE}/data/${selectedTicker}`);
            if (!priceRes.ok) throw new Error("Failed to fetch price data");
            const priceData = await priceRes.json();
            setStockData(priceData.data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        runAnalysis(ticker);
    }, [ticker]);

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 flex">
            {/* Sidebar */}
            <aside className="w-64 border-r border-slate-800 bg-slate-900/50 flex flex-col">
                <div className="p-6">
                    <div className="flex items-center gap-2 mb-8">
                        <div className="p-2 bg-emerald-500 rounded-lg">
                            <TrendingUp className="w-5 h-5 text-white" />
                        </div>
                        <h1 className="font-bold text-xl tracking-tight">Antigravity<span className="text-emerald-500">ML</span></h1>
                    </div>

                    <nav className="space-y-1">
                        <button className="w-full flex items-center gap-3 px-3 py-2 bg-emerald-500/10 text-emerald-400 rounded-lg text-sm font-medium">
                            <LayoutDashboard className="w-4 h-4" />
                            Overview
                        </button>
                        <button className="w-full flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 rounded-lg text-sm font-medium transition-colors">
                            <Activity className="w-4 h-4" />
                            Real-time
                        </button>
                        <button className="w-full flex items-center gap-3 px-3 py-2 text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 rounded-lg text-sm font-medium transition-colors">
                            <Wallet className="w-4 h-4" />
                            Portfolio
                        </button>
                    </nav>
                </div>

                <div className="mt-auto p-6 border-t border-slate-800">
                    <div className="bg-slate-800/50 rounded-xl p-4">
                        <p className="text-xs text-slate-500 mb-1">Current Balance</p>
                        <p className="text-lg font-bold text-white">$100,000.00</p>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto">
                {/* Header */}
                <header className="h-20 border-b border-slate-800 flex items-center justify-between px-8 bg-slate-900/30 backdrop-blur-md sticky top-0 z-10">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <select
                            title="Select Ticker"
                            value={ticker}
                            onChange={(e) => setTicker(e.target.value)}
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 appearance-none"
                        >
                            {tickers.map(t => <option key={t} value={t}>{t}</option>)}
                        </select>
                    </div>

                    <div className="flex items-center gap-4">
                        <button disabled={loading} onClick={() => runAnalysis(ticker)} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-lg shadow-emerald-500/20 disabled:opacity-50">
                            {loading ? 'Analyzing...' : 'Refresh Backtest'}
                        </button>
                    </div>
                </header>

                <div className="p-8 space-y-8 max-w-7xl mx-auto">
                    {error && (
                        <div className="p-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl flex items-center gap-3">
                            <ShieldAlert className="w-4 h-4" />
                            <p className="text-sm font-medium">{error}</p>
                        </div>
                    )}

                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <StatCard
                            label="Total Return"
                            value={backtestData ? `${(backtestData.metrics.total_return * 100).toFixed(2)}%` : '--'}
                            icon={TrendingUp}
                        />
                        <StatCard
                            label="Sharpe Ratio"
                            value={backtestData ? backtestData.metrics.sharpe_ratio.toFixed(2) : '--'}
                            icon={BarChart3}
                        />
                        <StatCard
                            label="Max Drawdown"
                            value={backtestData ? `${(backtestData.metrics.max_drawdown * 100).toFixed(2)}%` : '--'}
                            icon={ShieldAlert}
                        />
                        <StatCard
                            label="Profit Factor"
                            value={backtestData ? backtestData.metrics.profit_factor.toFixed(2) : '--'}
                            icon={Activity}
                        />
                        <StatCard
                            label="Win Rate"
                            value={backtestData ? `${(backtestData.metrics.win_rate * 100).toFixed(2)}%` : '--'}
                            icon={TrendingUp}
                        />
                        <StatCard
                            label="Total Trades"
                            value={backtestData ? backtestData.metrics.trades_count : '--'}
                            icon={ArrowRightLeft}
                        />
                    </div>

                    {/* Charts Section */}
                    <div className="grid grid-cols-1 gap-8">
                        <TradingChart
                            data={stockData}
                            equityData={backtestData?.equity_curve}
                        />
                    </div>

                    {/* Table Section */}
                    <div>
                        <TradeHistory trades={backtestData?.trades || []} />
                    </div>
                </div>
            </main>
        </div>
    );
}
