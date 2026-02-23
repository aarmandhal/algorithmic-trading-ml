import React from 'react';
import { LucideIcon } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface StatCardProps {
    label: string;
    value: string | number;
    icon: LucideIcon;
    trend?: {
        value: string;
        isPositive: boolean;
    };
    className?: string;
}

export function StatCard({ label, value, icon: Icon, trend, className }: StatCardProps) {
    return (
        <div className={cn("bg-slate-900/50 border border-slate-800 rounded-xl p-5 backdrop-blur-sm", className)}>
            <div className="flex items-center justify-between mb-3">
                <span className="text-slate-400 text-sm font-medium">{label}</span>
                <div className="p-2 bg-slate-800 rounded-lg">
                    <Icon className="w-5 h-5 text-emerald-400" />
                </div>
            </div>
            <div className="flex items-end justify-between">
                <h3 className="text-2xl font-bold text-white">{value}</h3>
                {trend && (
                    <span className={cn(
                        "text-xs font-semibold px-2 py-1 rounded-full",
                        trend.isPositive ? "bg-emerald-500/10 text-emerald-400" : "bg-rose-500/10 text-rose-400"
                    )}>
                        {trend.isPositive ? "+" : ""}{trend.value}
                    </span>
                )}
            </div>
        </div>
    );
}
