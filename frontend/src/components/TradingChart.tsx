'use client';

import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, CandlestickSeries, AreaSeries, IChartApi } from 'lightweight-charts';

interface ChartProps {
    data: any[];
    equityData?: any[];
    colors?: {
        backgroundColor?: string;
        lineColor?: string;
        textColor?: string;
        areaTopColor?: string;
        areaBottomColor?: string;
    };
}

export const TradingChart = ({
    data,
    equityData,
    colors: {
        backgroundColor = '#0f172a',
        lineColor = '#10b981',
        textColor = '#94a3b8',
        areaTopColor = '#10b981',
        areaBottomColor = 'rgba(16, 185, 129, 0.28)',
    } = {}
}: ChartProps) => {
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);

    useEffect(() => {
        if (!chartContainerRef.current) return;

        const handleResize = () => {
            chartRef.current?.applyOptions({ width: chartContainerRef.current!.clientWidth });
        };

        const chart = createChart(chartContainerRef.current, {
            layout: {
                background: { type: ColorType.Solid, color: backgroundColor },
                textColor,
            },
            width: chartContainerRef.current.clientWidth,
            height: 400,
            grid: {
                vertLines: { color: '#1e293b' },
                horzLines: { color: '#1e293b' },
            },
            timeScale: {
                borderColor: '#334155',
            },
        });

        chartRef.current = chart;

        const candlestickSeries = chart.addSeries(CandlestickSeries, {
            upColor: '#10b981',
            downColor: '#ef4444',
            borderVisible: false,
            wickUpColor: '#10b981',
            wickDownColor: '#ef4444',
        });

        // Transform data for lightweight-charts
        // data expected: list of {date, open, high, low, close}
        const formattedData = data.map(item => ({
            time: item.date,
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
        })).sort((a, b) => (a.time > b.time ? 1 : -1));

        candlestickSeries.setData(formattedData);

        if (equityData && equityData.length > 0) {
            const areaSeries = chart.addSeries(AreaSeries, {
                lineColor: '#3b82f6',
                topColor: 'rgba(59, 130, 246, 0.4)',
                bottomColor: 'rgba(59, 130, 246, 0.0)',
                lineWidth: 2,
                priceScaleId: 'left', // Use separate scale for equity
            });

            const formattedEquity = equityData.map(item => ({
                time: item.date,
                value: item.total_value,
            })).sort((a, b) => (a.time > b.time ? 1 : -1));

            areaSeries.setData(formattedEquity);

            chart.priceScale('left').applyOptions({
                autoScale: true,
                visible: true,
                borderColor: '#334155',
            });
        }

        chart.timeScale().fitContent();

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            chart.remove();
        };
    }, [data, equityData, backgroundColor, textColor]);

    return (
        <div className="w-full bg-slate-900/50 border border-slate-800 rounded-xl p-4 backdrop-blur-sm">
            <h3 className="text-slate-200 font-semibold mb-4 text-lg">Price & Strategy Performance</h3>
            <div ref={chartContainerRef} className="w-full h-[400px]" />
        </div>
    );
};
