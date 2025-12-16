// Generate comprehensive end-of-season player reports in professional Word document format.
// This mimics the type of reports that WNBA teams create for internal evaluation.

const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
        LevelFormat, PageBreak, ImageRun } = require('docx');

// Load player data from JSON (converted from CSV)
function loadPlayerData(csvPath) {
    const csv = fs.readFileSync(csvPath, 'utf-8');
    const lines = csv.split('\n');
    const headers = lines[0].split(',');
    
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
            const values = lines[i].split(',');
            const row = {};
            headers.forEach((header, idx) => {
                row[header.trim()] = values[idx] ? values[idx].trim() : '';
            });
            data.push(row);
        }
    }
    return data;
}

// Calculate comprehensive stats
function calculateStats(shotData) {
    const totalShots = shotData.length;
    const madeShots = shotData.filter(s => s.SHOT_MADE_FLAG === '1').length;
    const fgPct = ((madeShots / totalShots) * 100).toFixed(1);
    
    const twoPointers = shotData.filter(s => s.SHOT_TYPE === '2PT Field Goal');
    const twoMade = twoPointers.filter(s => s.SHOT_MADE_FLAG === '1').length;
    const twoPct = twoPointers.length > 0 ? ((twoMade / twoPointers.length) * 100).toFixed(1) : '0.0';
    
    const threePointers = shotData.filter(s => s.SHOT_TYPE === '3PT Field Goal');
    const threeMade = threePointers.filter(s => s.SHOT_MADE_FLAG === '1').length;
    const threePct = threePointers.length > 0 ? ((threeMade / threePointers.length) * 100).toFixed(1) : '0.0';
    
    // Quarter breakdown
    const quarters = {};
    [1, 2, 3, 4].forEach(q => {
        const qShots = shotData.filter(s => s.PERIOD === q.toString());
        const qMade = qShots.filter(s => s.SHOT_MADE_FLAG === '1').length;
        quarters[`Q${q}`] = {
            shots: qShots.length,
            pct: qShots.length > 0 ? ((qMade / qShots.length) * 100).toFixed(1) : '0.0'
        };
    });
    
    // Clutch stats (Q4, last 5 minutes = 300 seconds remaining)
    const clutchShots = shotData.filter(s => {
        if (s.PERIOD !== '4') return false;
        const mins = parseInt(s.MINUTES_REMAINING) || 0;
        const secs = parseInt(s.SECONDS_REMAINING) || 0;
        const totalSecs = (mins * 60) + secs;
        return totalSecs <= 300;
    });
    const clutchMade = clutchShots.filter(s => s.SHOT_MADE_FLAG === '1').length;
    const clutchPct = clutchShots.length > 0 ? ((clutchMade / clutchShots.length) * 100).toFixed(1) : '0.0';
    
    return {
        totalShots,
        madeShots,
        fgPct,
        twoAttempts: twoPointers.length,
        twoMade,
        twoPct,
        threeAttempts: threePointers.length,
        threeMade,
        threePct,
        quarters,
        clutch: {
            shots: clutchShots.length,
            made: clutchMade,
            pct: clutchPct
        }
    };
}

function createPlayerReport(playerName, csvPath, imagePaths = {}) {
    const shotData = loadPlayerData(csvPath);
    const stats = calculateStats(shotData);
    const playerFirstName = playerName.split(' ')[0];
    
    // Define table border style
    const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
    const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };
    
    const doc = new Document({
        styles: {
            default: {
                document: { run: { font: "Arial", size: 22 } } // 11pt default
            },
            paragraphStyles: [
                {
                    id: "Title",
                    name: "Title",
                    basedOn: "Normal",
                    run: { size: 56, bold: true, color: "002B5C", font: "Arial" },
                    paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER }
                },
                {
                    id: "Heading1",
                    name: "Heading 1",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 32, bold: true, color: "002B5C", font: "Arial" },
                    paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 }
                },
                {
                    id: "Heading2",
                    name: "Heading 2",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 28, bold: true, color: "002B5C", font: "Arial" },
                    paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
                },
                {
                    id: "Heading3",
                    name: "Heading 3",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 24, bold: true, color: "002B5C", font: "Arial" },
                    paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 2 }
                }
            ]
        },
        numbering: {
            config: [
                {
                    reference: "bullet-list",
                    levels: [{
                        level: 0,
                        format: LevelFormat.BULLET,
                        text: "•",
                        alignment: AlignmentType.LEFT,
                        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
                    }]
                },
                {
                    reference: "recommendations-list",
                    levels: [{
                        level: 0,
                        format: LevelFormat.DECIMAL,
                        text: "%1.",
                        alignment: AlignmentType.LEFT,
                        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
                    }]
                }
            ]
        },
        sections: [{
            properties: {
                page: {
                    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
                }
            },
            children: [
                // TITLE PAGE
                new Paragraph({
                    heading: HeadingLevel.TITLE,
                    children: [new TextRun(`${playerName}`)]
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 120 },
                    children: [new TextRun({
                        text: "2025 Season Performance Analysis",
                        size: 32,
                        bold: true,
                        color: "6ECEB2"
                    })]
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 360 },
                    children: [new TextRun({
                        text: "New York Liberty Basketball Operations",
                        size: 24,
                        italics: true
                    })]
                }),
                
                // EXECUTIVE SUMMARY
                new Paragraph({
                    heading: HeadingLevel.HEADING_1,
                    children: [new TextRun("Executive Summary")]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(`This report provides a comprehensive analysis of ${playerName}'s shooting performance during the 2025 WNBA regular season. The analysis examines overall efficiency, shot selection patterns, situational performance, and provides data-driven recommendations for the 2026 season.`)]
                }),
                
                // KEY STATISTICS TABLE
                new Paragraph({
                    heading: HeadingLevel.HEADING_2,
                    children: [new TextRun("Season Statistics Overview")]
                }),
                new Table({
                    columnWidths: [3120, 3120, 3120],
                    margins: { top: 100, bottom: 100, left: 180, right: 180 },
                    rows: [
                        new TableRow({
                            tableHeader: true,
                            children: [
                                new TableCell({
                                    borders: cellBorders,
                                    width: { size: 3120, type: WidthType.DXA },
                                    shading: { fill: "002B5C", type: ShadingType.CLEAR },
                                    children: [new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        children: [new TextRun({ text: "Metric", bold: true, color: "FFFFFF" })]
                                    })]
                                }),
                                new TableCell({
                                    borders: cellBorders,
                                    width: { size: 3120, type: WidthType.DXA },
                                    shading: { fill: "002B5C", type: ShadingType.CLEAR },
                                    children: [new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        children: [new TextRun({ text: "Value", bold: true, color: "FFFFFF" })]
                                    })]
                                }),
                                new TableCell({
                                    borders: cellBorders,
                                    width: { size: 3120, type: WidthType.DXA },
                                    shading: { fill: "002B5C", type: ShadingType.CLEAR },
                                    children: [new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        children: [new TextRun({ text: "League Comparison", bold: true, color: "FFFFFF" })]
                                    })]
                                })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Total Field Goal Attempts")] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(stats.totalShots.toString())] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: stats.totalShots >= 350 ? "High Volume" : stats.totalShots >= 250 ? "Moderate Volume" : "Low Volume", color: stats.totalShots >= 350 ? "2E7D32" : stats.totalShots >= 250 ? "666666" : "C62828" })] })] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Field Goal Percentage", bold: true })] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${stats.fgPct}%`, bold: true })] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: parseFloat(stats.fgPct) >= 43.9 ? "Above Avg (43.9%)" : "Below Avg (43.9%)", color: parseFloat(stats.fgPct) >= 43.9 ? "2E7D32" : "C62828" })] })] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("2-Point Percentage")] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(`${stats.twoPct}%`)] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: parseFloat(stats.twoPct) >= 49.8 ? "Above Avg (49.8%)" : "Below Avg (49.8%)", color: parseFloat(stats.twoPct) >= 49.8 ? "2E7D32" : "C62828" })] })] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun("3-Point Percentage")] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun(`${stats.threePct}%`)] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: parseFloat(stats.threePct) >= 33.8 ? "Above Avg (33.8%)" : "Below Avg (33.8%)", color: parseFloat(stats.threePct) >= 33.8 ? "2E7D32" : "C62828" })] })] })
                            ]
                        }),
                        new TableRow({
                            children: [
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Clutch FG% (Last 5 min Q4)", bold: true })] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${stats.clutch.pct}%`, bold: true })] })] }),
                                new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: stats.clutch.shots >= 10 ? (parseFloat(stats.clutch.pct) >= 42.0 ? "Above Avg (42.0%)" : "Below Avg (42.0%)") : "Small Sample", color: stats.clutch.shots >= 10 ? (parseFloat(stats.clutch.pct) >= 42.0 ? "2E7D32" : "C62828") : "666666" })] })] })
                            ]
                        })
                    ]
                }),
                new Paragraph({ children: [new TextRun("")] }), // Spacing
                
                // QUARTER BREAKDOWN
                new Paragraph({
                    heading: HeadingLevel.HEADING_2,
                    children: [new TextRun("Performance by Quarter")]
                }),
                new Table({
                    columnWidths: [2340, 2340, 2340, 2340],
                    margins: { top: 100, bottom: 100, left: 180, right: 180 },
                    rows: [
                        new TableRow({
                            tableHeader: true,
                            children: ['Q1', 'Q2', 'Q3', 'Q4'].map(q => 
                                new TableCell({
                                    borders: cellBorders,
                                    width: { size: 2340, type: WidthType.DXA },
                                    shading: { fill: "6ECEB2", type: ShadingType.CLEAR },
                                    children: [new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        children: [new TextRun({ text: q, bold: true })]
                                    })]
                                })
                            )
                        }),
                        new TableRow({
                            children: [1, 2, 3, 4].map(q => 
                                new TableCell({
                                    borders: cellBorders,
                                    width: { size: 2340, type: WidthType.DXA },
                                    children: [new Paragraph({
                                        alignment: AlignmentType.CENTER,
                                        children: [new TextRun({
                                            text: `${stats.quarters[`Q${q}`].pct}% (${stats.quarters[`Q${q}`].shots} FGA)`,
                                            size: 20
                                        })]
                                    })]
                                })
                            )
                        })
                    ]
                }),
                new Paragraph({ children: [new TextRun("")] }), // Spacing
                
                // PAGE BREAK
                new Paragraph({ children: [new PageBreak()] }),
                
                // SHOT CHART IMAGE
                new Paragraph({
                    heading: HeadingLevel.HEADING_1,
                    children: [new TextRun("Shot Distribution Analysis")]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(`The shot chart below illustrates ${playerFirstName}'s shot locations throughout the 2025 season. Green markers indicate made shots, while red markers indicate misses. This visualization reveals shooting tendencies and efficiency across different court zones.`)]
                }),
                ...(imagePaths.shotChart ? [
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 120, after: 240 },
                        children: [new ImageRun({
                            type: "png",
                            data: fs.readFileSync(imagePaths.shotChart),
                            transformation: { width: 500, height: 458 },
                            altText: { title: "Shot Chart", description: `${playerName} shot distribution`, name: "shot_chart" }
                        })]
                    })
                ] : []),
                
                // CLUTCH PERFORMANCE ANALYSIS
                new Paragraph({
                    heading: HeadingLevel.HEADING_2,
                    children: [new TextRun("Clutch Performance Analysis")]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(`${playerFirstName} attempted ${stats.clutch.shots} shots in clutch situations (last 5 minutes of 4th quarter in close games), converting ${stats.clutch.made} for a ${stats.clutch.pct}% field goal percentage.`)]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(`This represents a ${parseFloat(stats.clutch.pct) > parseFloat(stats.fgPct) ? 'POSITIVE' : 'NEGATIVE'} differential of ${Math.abs(parseFloat(stats.clutch.pct) - parseFloat(stats.fgPct)).toFixed(1)} percentage points compared to overall season efficiency.`)]
                }),
                
                // KEY OBSERVATIONS
                new Paragraph({
                    heading: HeadingLevel.HEADING_2,
                    children: [new TextRun("Key Observations")]
                }),
                new Paragraph({
                    numbering: { reference: "bullet-list", level: 0 },
                    children: [new TextRun(`Shot volume: ${stats.totalShots} attempts across ${shotData.filter((v, i, a) => a.findIndex(t => t.GAME_ID === v.GAME_ID) === i).length} games (avg ${(stats.totalShots / shotData.filter((v, i, a) => a.findIndex(t => t.GAME_ID === v.GAME_ID) === i).length).toFixed(1)} FGA/game)`)]
                }),
                new Paragraph({
                    numbering: { reference: "bullet-list", level: 0 },
                    children: [new TextRun(`Shot selection: ${((stats.threeAttempts / stats.totalShots) * 100).toFixed(1)}% of attempts from 3-point range`)]
                }),
                new Paragraph({
                    numbering: { reference: "bullet-list", level: 0 },
                    children: [new TextRun(`${parseFloat(stats.twoPct) > parseFloat(stats.threePct) ? 'More efficient' : 'Less efficient'} inside the arc (${stats.twoPct}% 2PT vs ${stats.threePct}% 3PT)`)]
                }),
                new Paragraph({
                    numbering: { reference: "bullet-list", level: 0 },
                    children: [new TextRun(`Q${Object.keys(stats.quarters).reduce((a, b) => parseFloat(stats.quarters[a].pct) > parseFloat(stats.quarters[b].pct) ? a : b).substring(1)} was strongest quarter (${Math.max(...Object.values(stats.quarters).map(q => parseFloat(q.pct)))}% FG)`)]
                }),
                
                // PAGE BREAK
                new Paragraph({ children: [new PageBreak()] }),
                
                // RECOMMENDATIONS
                new Paragraph({
                    heading: HeadingLevel.HEADING_1,
                    children: [new TextRun("Development Recommendations for 2026")]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(`Based on ${playerFirstName}'s 2025 performance data, the following areas present opportunities for development and optimization:`)]
                }),
                
                // Dynamic recommendations based on stats
                ...(parseFloat(stats.threePct) < 35 ? [
                    new Paragraph({
                        numbering: { reference: "recommendations-list", level: 0 },
                        children: [new TextRun({ text: "Shot Selection: ", bold: true }), new TextRun(`Three-point efficiency (${stats.threePct}%) is significantly below two-point efficiency (${stats.twoPct}%). Recommend working with coaching staff to identify higher-quality three-point looks or increasing paint touches where ${playerFirstName} is more efficient. Focus on catch-and-shoot opportunities vs. off-the-dribble attempts.`)]
                    })
                ] : [
                    new Paragraph({
                        numbering: { reference: "recommendations-list", level: 0 },
                        children: [new TextRun({ text: "Shot Selection: ", bold: true }), new TextRun(`Strong three-point efficiency (${stats.threePct}%) suggests ability to stretch the floor effectively. Continue emphasizing perimeter spacing while maintaining versatility with ${stats.twoPct}% efficiency on two-point attempts.`)]
                    })
                ]),
                
                ...(parseFloat(stats.clutch.pct) < parseFloat(stats.fgPct) - 5 ? [
                    new Paragraph({
                        numbering: { reference: "recommendations-list", level: 0 },
                        children: [new TextRun({ text: "Late-Game Execution: ", bold: true }), new TextRun(`Clutch shooting (${stats.clutch.pct}%) drops ${Math.abs(parseFloat(stats.clutch.pct) - parseFloat(stats.fgPct)).toFixed(1)} percentage points below season average. Recommend increased practice repetitions simulating late-game pressure situations. Focus on shot quality over volume in final possessions. Consider film study of successful clutch sequences to identify patterns in shot creation and selection.`)]
                    })
                ] : parseFloat(stats.clutch.pct) > parseFloat(stats.fgPct) + 3 ? [
                    new Paragraph({
                        numbering: { reference: "recommendations-list", level: 0 },
                        children: [new TextRun({ text: "Late-Game Execution: ", bold: true }), new TextRun(`Clutch performance (${stats.clutch.pct}%) exceeds season average by ${(parseFloat(stats.clutch.pct) - parseFloat(stats.fgPct)).toFixed(1)} points—demonstrating excellent composure under pressure. This is a competitive advantage to leverage in critical possessions. Consider increased usage in late-game situations.`)]
                    })
                ] : []),
                
                // Quarter-specific recommendations
                ...(Object.entries(stats.quarters).some(([q, data]) => parseFloat(data.pct) < parseFloat(stats.fgPct) - 5) ? [
                    new Paragraph({
                        numbering: { reference: "recommendations-list", level: 0 },
                        children: [new TextRun({ text: "Conditioning & Consistency: ", bold: true }), new TextRun(`Performance variance across quarters suggests potential fatigue or rhythm factors. ${Object.entries(stats.quarters).sort((a, b) => parseFloat(a[1].pct) - parseFloat(b[1].pct))[0][0]} efficiency (${Object.entries(stats.quarters).sort((a, b) => parseFloat(a[1].pct) - parseFloat(b[1].pct))[0][1].pct}%) is notably lower than ${Object.entries(stats.quarters).sort((a, b) => parseFloat(b[1].pct) - parseFloat(a[1].pct))[0][0]} (${Object.entries(stats.quarters).sort((a, b) => parseFloat(b[1].pct) - parseFloat(a[1].pct))[0][1].pct}%). Evaluate warm-up routines, in-game rest patterns, and conditioning protocols to maintain consistent performance.`)]
                    })
                ] : []),
                
                new Paragraph({
                    numbering: { reference: "recommendations-list", level: 0 },
                    children: [new TextRun({ text: "Film Study Focus: ", bold: true }), new TextRun("Conduct detailed review of missed shots by court location to identify mechanical adjustments or defensive coverage patterns. Pay particular attention to sequences where efficiency deviated significantly from season averages.")]
                }),
                
                new Paragraph({
                    numbering: { reference: "recommendations-list", level: 0 },
                    children: [new TextRun({ text: "Off-Season Development: ", bold: true }), new TextRun("Work with player development staff to create targeted shooting workouts that replicate game conditions in lower-efficiency zones. Incorporate decision-making drills that emphasize shot quality assessment under time pressure.")]
                }),
                
                // CLOSING
                new Paragraph({
                    spacing: { before: 360, after: 120 },
                    children: [new TextRun("")]
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { before: 240 },
                    children: [new TextRun({
                        text: "Report generated using official WNBA Stats API data",
                        size: 18,
                        italics: true,
                        color: "666666"
                    })]
                })
            ]
        }]
    });
    
    return doc;
}

// Generate report
const playerName = process.argv[2] || "Sabrina Ionescu";
const csvPath = process.argv[3] || "/home/claude/wnba-shot-analysis/data/raw/ionescu_shots_2025.csv";
const shotChartPath = process.argv[4] || "/home/claude/wnba-shot-analysis/outputs/shot_charts/real/Ionescu_2025_REAL_shotchart.png";
const outputPath = process.argv[5] || "/home/claude/wnba-shot-analysis/outputs/player_reports/Ionescu_2025_Season_Report.docx";

console.log(`\nGenerating player report for ${playerName}...`);
console.log(`Data source: ${csvPath}`);
console.log(`Output: ${outputPath}\n`);

const doc = createPlayerReport(playerName, csvPath, { shotChart: shotChartPath });

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`✅ Report generated successfully!`);
    console.log(`📄 File: ${outputPath}\n`);
});
