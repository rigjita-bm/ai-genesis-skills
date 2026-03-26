#!/usr/bin/env python3
"""
Lab Protocol Optimizer — AI-powered optimization for biological laboratory protocols
Specialized skill for biotech labs, research facilities, and diagnostic centers
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Protocol templates for common bio-lab procedures
PROTOCOL_TEMPLATES = {
    "pcr": {
        "name": "PCR (Polymerase Chain Reaction)",
        "steps": [
            "Denaturation (94-98°C, 30s-2min)",
            "Annealing (50-65°C, 20-40s)",
            "Extension (72°C, 1min per 1kb)",
            "Final Extension (72°C, 5-10min)"
        ],
        "optimization_params": ["MgCl2 concentration", "Annealing temp", "Cycle number", "Template amount"],
        "common_issues": ["Non-specific amplification", "Primer dimers", "Low yield", "Smearing"]
    },
    "gel_electrophoresis": {
        "name": "Gel Electrophoresis",
        "steps": [
            "Prepare gel with appropriate agarose %",
            "Load samples with loading dye",
            "Run at constant voltage (5-10 V/cm)",
            "Stain and visualize"
        ],
        "optimization_params": ["Agarose concentration", "Voltage", "Run time", "Buffer type"],
        "common_issues": ["Poor resolution", "Band smiling", "DNA diffusion", "Uneven migration"]
    },
    "cell_culture": {
        "name": "Cell Culture Maintenance",
        "steps": [
            "Warm media and reagents",
            "Aspirate old media",
            "Wash with PBS",
            "Add trypsin for adherent cells",
            "Neutralize and split cells"
        ],
        "optimization_params": ["Seeding density", "Media composition", "Passage ratio", "Incubation time"],
        "common_issues": ["Contamination", "Slow growth", "Differentiation", "Detachment"]
    },
    "protein_purification": {
        "name": "Protein Purification (Chromatography)",
        "steps": [
            "Column equilibration",
            "Sample loading",
            "Washing unbound proteins",
            "Elution with gradient",
            "Collection and analysis"
        ],
        "optimization_params": ["Buffer pH", "Salt concentration", "Flow rate", "Column type"],
        "common_issues": ["Low purity", "Protein precipitation", "Column clogging", "Activity loss"]
    },
    "dna_extraction": {
        "name": "DNA Extraction",
        "steps": [
            "Cell lysis",
            "Protein digestion",
            "DNA precipitation",
            "Washing",
            "Resuspension"
        ],
        "optimization_params": ["Lysis buffer strength", "Incubation time", "Ethanol concentration", "Elution volume"],
        "common_issues": ["Low yield", "RNA contamination", "Degraded DNA", "PCR inhibitors"]
    },
    "western_blot": {
        "name": "Western Blot",
        "steps": [
            "Protein separation by SDS-PAGE",
            "Transfer to membrane",
            "Blocking",
            "Primary antibody incubation",
            "Secondary antibody incubation",
            "Detection"
        ],
        "optimization_params": ["Acrylamide %", "Transfer conditions", "Blocking agent", "Antibody dilution"],
        "common_issues": ["High background", "Weak signal", "Non-specific bands", "Uneven transfer"]
    }
}

# AI suggestions database
OPTIMIZATION_STRATEGIES = {
    "time_reduction": [
        "Use faster polymerases for PCR (reduce extension time by 50%)",
        "Implement master mixes to reduce pipetting steps",
        "Parallel processing of multiple samples",
        "Automated liquid handling for repetitive steps",
        "Pre-made aliquots of common reagents"
    ],
    "cost_reduction": [
        "Optimize reagent concentrations (often can use 0.5-0.7x recommended)",
        "Recycle buffers where possible (e.g., electrophoresis buffer)",
        "Bulk purchasing with proper storage",
        "Reduce reaction volumes (miniaturization)",
        "In-house preparation of common reagents"
    ],
    "quality_improvement": [
        "Implement positive and negative controls in every run",
        "Use calibrated pipettes and regular maintenance",
        "Environmental monitoring (temperature, humidity)",
        "Standardized SOPs with version control",
        "Regular proficiency testing"
    ],
    "error_prevention": [
        "Barcode sample tracking system",
        "Automated pipetting to reduce human error",
        "Double-check protocols with checklists",
        "Real-time monitoring with IoT sensors",
        "AI-assisted image analysis for results"
    ]
}


def analyze_protocol(protocol_type: str, current_issues: List[str] = None) -> Dict:
    """Analyze a lab protocol and suggest optimizations"""
    
    if protocol_type not in PROTOCOL_TEMPLATES:
        return {
            "error": f"Unknown protocol. Available: {', '.join(PROTOCOL_TEMPLATES.keys())}"
        }
    
    template = PROTOCOL_TEMPLATES[protocol_type]
    
    analysis = {
        "protocol_name": template["name"],
        "current_steps": template["steps"],
        "optimization_focus": template["optimization_params"],
        "identified_issues": current_issues or template["common_issues"][:2],
        "suggestions": {
            "time_saving": OPTIMIZATION_STRATEGIES["time_reduction"][:3],
            "cost_saving": OPTIMIZATION_STRATEGIES["cost_reduction"][:3],
            "quality": OPTIMIZATION_STRATEGIES["quality_improvement"][:3],
            "error_prevention": OPTIMIZATION_STRATEGIES["error_prevention"][:3]
        },
        "automation_opportunities": identify_automation(protocol_type),
        "ai_integration": suggest_ai_tools(protocol_type)
    }
    
    return analysis


def identify_automation(protocol_type: str) -> List[str]:
    """Identify automation opportunities for a protocol"""
    
    automation_map = {
        "pcr": [
            "Automated liquid handling for master mix preparation",
            "Robotic sample loading into thermocycler",
            "Automated result analysis (qPCR curves)",
            "Integration with LIMS for result reporting"
        ],
        "gel_electrophoresis": [
            "Automated gel casting systems",
            "Robotic sample loading",
            "Automated imaging and analysis",
            "Digital gel documentation with AI sizing"
        ],
        "cell_culture": [
            "Automated cell counters (Trypan blue/fluorescence)",
            "Media exchange robots",
            "Incubator monitoring systems",
            "Automated passage scheduling"
        ],
        "protein_purification": [
            "FPLC/AKTA automation systems",
            "Fraction collectors with UV monitoring",
            "Automated buffer preparation",
            "Peak detection and pooling algorithms"
        ],
        "dna_extraction": [
            "Magnetic bead-based automated extractors",
            "Liquid handling robots",
            "Quality control with automated spectrophotometry",
            "Sample tracking with barcode integration"
        ],
        "western_blot": [
            "Semi-dry transfer systems",
            "Automated western blot processors",
            "Imaging systems with AI band quantification",
            "Digital workflow documentation"
        ]
    }
    
    return automation_map.get(protocol_type, ["General liquid handling automation", "Sample tracking systems"])


def suggest_ai_tools(protocol_type: str) -> List[Dict]:
    """Suggest AI tools for protocol optimization"""
    
    ai_tools = {
        "pcr": [
            {"tool": "Primer3 / NCBI Primer-BLAST", "use": "Optimal primer design", "cost": "Free"},
            {"tool": "Benchling / SnapGene", "use": "Protocol design and sharing", "cost": "Freemium"},
            {"tool": "Custom ML model", "use": "Predict optimal annealing temps", "cost": "Development"}
        ],
        "gel_electrophoresis": [
            {"tool": "ImageJ / GelAnalyzer", "use": "Band quantification", "cost": "Free"},
            {"tool": "LabGuru", "use": "Protocol management", "cost": "Subscription"},
            {"tool": "Computer vision model", "use": "Automated band calling", "cost": "Development"}
        ],
        "cell_culture": [
            {"tool": "IncuCyte", "use": "Live cell imaging and analysis", "cost": "High (equipment)"},
            {"tool": "CellProfiler", "use": "Image analysis", "cost": "Free"},
            {"tool": "Predictive growth models", "use": "Optimal passage timing", "cost": "Development"}
        ],
        "protein_purification": [
            {"tool": "Unicorn / ChromLab software", "use": "Chromatography control", "cost": "Included with equipment"},
            {"tool": "AI peak detection", "use": "Automated fraction collection", "cost": "Development"},
            {"tool": "Buffer optimization ML", "use": "Predict optimal conditions", "cost": "Development"}
        ],
        "dna_extraction": [
            {"tool": "Nanodrop / Qubit", "use": "Quality control", "cost": "Equipment"},
            {"tool": "LIMS integration", "use": "Sample tracking", "cost": "Variable"},
            {"tool": "Yield prediction model", "use": "Predict DNA concentration", "cost": "Development"}
        ],
        "western_blot": [
            {"tool": "Image Studio / ImageJ", "use": "Band analysis", "cost": "Free/Paid"},
            {"tool": "AI background subtraction", "use": "Cleaner quantification", "cost": "Development"},
            {"tool": "Protocol optimization", "use": "Antibody titer prediction", "cost": "Development"}
        ]
    }
    
    return ai_tools.get(protocol_type, [
        {"tool": "ELN (Electronic Lab Notebook)", "use": "Protocol documentation", "cost": "Freemium"},
        {"tool": "LIMS", "use": "Sample management", "cost": "Variable"}
    ])


def generate_optimization_report(protocol_type: str, lab_size: str = "small", budget: str = "medium") -> str:
    """Generate comprehensive optimization report"""
    
    analysis = analyze_protocol(protocol_type)
    
    if "error" in analysis:
        return analysis["error"]
    
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🔬 LAB PROTOCOL OPTIMIZATION REPORT                             ║
║  {analysis['protocol_name']:<56} ║
║  Lab Size: {lab_size.upper():<8} | Budget: {budget.upper():<8}                        ║
╚══════════════════════════════════════════════════════════════════╝

📋 CURRENT PROTOCOL OVERVIEW
───────────────────────────────────────────────────────────────────
"""
    
    for i, step in enumerate(analysis['current_steps'], 1):
        report += f"{i}. {step}\n"
    
    report += f"""
⚠️  IDENTIFIED ISSUES / OPTIMIZATION FOCUS
───────────────────────────────────────────────────────────────────
"""
    for issue in analysis['identified_issues']:
        report += f"• {issue}\n"
    
    report += f"""
🎯 KEY OPTIMIZATION PARAMETERS
───────────────────────────────────────────────────────────────────
"""
    for param in analysis['optimization_focus']:
        report += f"• {param}\n"
    
    report += """
⏱️  TIME-SAVING SUGGESTIONS
───────────────────────────────────────────────────────────────────
"""
    for suggestion in analysis['suggestions']['time_saving']:
        report += f"✓ {suggestion}\n"
    
    report += """
💰 COST-REDUCTION STRATEGIES
───────────────────────────────────────────────────────────────────
"""
    for suggestion in analysis['suggestions']['cost_saving']:
        report += f"✓ {suggestion}\n"
    
    report += """
🔬 QUALITY IMPROVEMENTS
───────────────────────────────────────────────────────────────────
"""
    for suggestion in analysis['suggestions']['quality']:
        report += f"✓ {suggestion}\n"
    
    report += """
🤖 AUTOMATION OPPORTUNITIES
───────────────────────────────────────────────────────────────────
"""
    for auto in analysis['automation_opportunities']:
        report += f"• {auto}\n"
    
    report += """
🧠 AI TOOLS INTEGRATION
───────────────────────────────────────────────────────────────────
"""
    for tool in analysis['ai_integration']:
        report += f"• {tool['tool']}\n  Use: {tool['use']}\n  Cost: {tool['cost']}\n\n"
    
    # Budget-specific recommendations
    report += generate_budget_recommendations(budget)
    
    report += """
📊 IMPLEMENTATION ROADMAP
───────────────────────────────────────────────────────────────────
Phase 1 (Week 1-2): Document current protocol variations
Phase 2 (Week 3-4): Implement quick wins (master mixes, checklists)
Phase 3 (Month 2): Pilot automation tools
Phase 4 (Month 3+): AI integration and continuous optimization

💡 EXPECTED OUTCOMES
───────────────────────────────────────────────────────────────────
• Time reduction: 20-40%
• Cost reduction: 15-30%
• Error rate reduction: 50-70%
• Reproducibility improvement: 30-50%

Generated by AI Genesis Lab Protocol Optimizer
"""
    
    return report


def generate_budget_recommendations(budget: str) -> str:
    """Generate budget-specific recommendations"""
    
    recommendations = {
        "low": """
💵 LOW-BUDGET RECOMMENDATIONS
───────────────────────────────────────────────────────────────────
• Use free software: ImageJ, CellProfiler, Primer3
• Implement SOPs and checklists (zero cost)
• Create master mixes to reduce pipetting errors
• Use Google Sheets/Airtable for sample tracking
• Join core facilities for expensive equipment access
• DIY automation with Arduino/Raspberry Pi
""",
        "medium": """
💵 MEDIUM-BUDGET RECOMMENDATIONS
───────────────────────────────────────────────────────────────────
• Electronic Lab Notebook (Benchling, LabArchives)
• Basic liquid handling robot (OT-2 or similar)
• Automated cell counter
• Cloud-based LIMS ( affordable tiers)
• Staff training on automation tools
• Contract bioinformatics for custom scripts
""",
        "high": """
💵 HIGH-BUDGET RECOMMENDATIONS
───────────────────────────────────────────────────────────────────
• Full automation platform (Tecan, Hamilton)
• Integrated LIMS with AI capabilities
• Robotics for routine protocols
• Custom ML model development
• Dedicated automation specialist
• Continuous monitoring IoT infrastructure
"""
    }
    
    return recommendations.get(budget, recommendations["medium"])


def create_protocol_template(protocol_name: str, steps: List[str]) -> str:
    """Create a new protocol template"""
    
    template = f"""
# {protocol_name} — Standard Operating Procedure

## Purpose
[Brief description of what this protocol accomplishes]

## Materials
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Equipment
- [ ] Equipment 1
- [ ] Equipment 2

## Procedure
"""
    
    for i, step in enumerate(steps, 1):
        template += f"\n### Step {i}: {step}\n"
        template += f"**Duration:** [X minutes/hours]\n"
        template += f"**Critical points:** [What can go wrong]\n"
        template += f"**Notes:** [Additional information]\n"
    
    template += """
## Quality Control
- [ ] Positive control: [Description]
- [ ] Negative control: [Description]
- [ ] Expected result: [Description]

## Troubleshooting
| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| [Problem 1] | [Cause] | [Solution] |
| [Problem 2] | [Cause] | [Solution] |

## Safety Considerations
⚠️ [List safety hazards and precautions]

## Version Control
- v1.0: [Date] — Initial version
- v1.1: [Date] — [Changes]

---
Document created by AI Genesis Lab Protocol Optimizer
"""
    
    return template


def main():
    parser = argparse.ArgumentParser(description="Lab Protocol Optimizer for Biological Labs")
    parser.add_argument("protocol", nargs="?", help="Protocol type (pcr, gel_electrophoresis, cell_culture, etc.)")
    parser.add_argument("--lab-size", "-s", default="small", choices=["small", "medium", "large"],
                       help="Laboratory size")
    parser.add_argument("--budget", "-b", default="medium", choices=["low", "medium", "high"],
                       help="Available budget")
    parser.add_argument("--issues", "-i", nargs="+", help="Current issues (space-separated)")
    parser.add_argument("--template", "-t", action="store_true", help="Generate SOP template")
    parser.add_argument("--save", action="store_true", help="Save report to file")
    
    args = parser.parse_args()
    
    if not args.protocol:
        print("🔬 Lab Protocol Optimizer — AI для биологических лабораторий")
        print()
        print("Доступные протоколы:")
        for key, value in PROTOCOL_TEMPLATES.items():
            print(f"  • {key}: {value['name']}")
        print()
        print("Примеры:")
        print('  genesis lab pcr --lab-size small --budget medium')
        print('  genesis lab cell_culture --issues "slow_growth contamination"')
        print('  genesis lab dna_extraction --template')
        return
    
    if args.template:
        protocol_info = PROTOCOL_TEMPLATES.get(args.protocol)
        if protocol_info:
            template = create_protocol_template(
                protocol_info['name'],
                protocol_info['steps']
            )
            print(template)
            
            if args.save:
                output_dir = "/root/.openclaw/output/lab-protocols"
                os.makedirs(output_dir, exist_ok=True)
                filename = f"{args.protocol}_sop_template.md"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(template)
                print(f"\n💾 Сохранено: {filepath}")
        else:
            print(f"❌ Неизвестный протокол: {args.protocol}")
        return
    
    # Generate optimization report
    report = generate_optimization_report(args.protocol, args.lab_size, args.budget)
    print(report)
    
    if args.save:
        output_dir = "/root/.openclaw/output/lab-protocols"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{args.protocol}_optimization_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(report)
        print(f"\n💾 Отчёт сохранён: {filepath}")


if __name__ == "__main__":
    main()
