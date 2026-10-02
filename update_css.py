import re

with open('panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new CSS
new_css = """<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';padding:20px;max-width:1200px;margin:0 auto;min-height:100vh}
h1{font-size:1.5em;margin-bottom:8px;color:#38bdf8;text-transform:uppercase;letter-spacing:2px;font-weight:700}
.sub{color:#94a3b8;font-size:0.85em;margin-bottom:24px}
.panel-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}

.card{border:1px solid #334155;border-radius:8px;padding:20px;background:#1e293b;position:relative;box-shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);transition:transform 0.2s, box-shadow 0.2s}
.card:hover{transform:translateY(-2px);box-shadow:0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)}
.card.gemini{border-top:3px solid #38bdf8}
.card.claude{border-top:3px solid #818cf8}
.card-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.indicator{width:12px;height:12px;border-radius:50%;display:inline-block}
.indicator.alive{background:#10b981;box-shadow:0 0 8px rgba(16, 185, 129, 0.6)}
.indicator.dead{background:#ef4444;box-shadow:0 0 8px rgba(239, 68, 68, 0.6)}
.indicator.unknown{background:#64748b}
@keyframes pulse{0%{opacity:1}50%{opacity:0.6}100%{opacity:1}}
.card-title{font-size:1.1em;font-weight:bold;text-transform:uppercase;letter-spacing:1px}
.card-title .gemini{color:#38bdf8}
.card-title .claude{color:#818cf8}
.card-body{font-size:0.85em;color:#cbd5e1;line-height:1.7}
.card-body .row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #334155}
.card-body .row:last-child{border:none}
.card-body .label{color:#94a3b8;font-weight:500}
.card-body .value{color:#f8fafc;font-weight:600}
.card-body .value.warn{color:#f59e0b}
.card-body .value.critical{color:#ef4444}
.actions{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}
.installed-actions{display:flex;gap:10px;flex-wrap:wrap}
.missing-actions{display:none;gap:10px;flex-wrap:wrap}

.btn{background:#334155;border:1px solid #475569;border-radius:6px;color:#f8fafc;padding:8px 16px;cursor:pointer;font-family:inherit;font-size:0.8em;font-weight:600;transition:all 0.2s;display:inline-flex;align-items:center;justify-content:center}
.btn:hover{background:#475569;border-color:#64748b;transform:translateY(-1px)}
.btn:active{transform:translateY(0)}
.btn.danger{background:#7f1d1d;border-color:#991b1b;color:#fca5a5}
.btn.danger:hover{background:#991b1b;border-color:#b91c1c}
.btn.warning{background:#78350f;border-color:#92400e;color:#fcd34d}
.btn.warning:hover{background:#92400e;border-color:#b45309}
.btn.primary{background:#0284c7;border-color:#0369a1;color:#ffffff}
.btn.primary:hover{background:#0369a1;border-color:#075985}
.btn:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.btn.small{padding:4px 10px;font-size:0.75em}

.btn[title]{position:relative}
.btn[title]:hover::after{content:attr(title);position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#0f172a;color:#cbd5e1;border:1px solid #334155;border-radius:4px;padding:6px 10px;font-size:0.85em;font-weight:normal;white-space:nowrap;z-index:10;pointer-events:none;box-shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1)}

.section-title{color:#38bdf8;font-size:1em;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin:30px 0 16px;border-bottom:2px solid #1e293b;padding-bottom:8px}

.log-box{background:#0f172a;border:1px solid #334155;border-radius:6px;padding:12px;font-size:0.75em;font-family:'Courier New', Consolas, monospace;line-height:1.4;height:250px;overflow-y:auto;white-space:pre-wrap;word-break:break-all;color:#94a3b8;box-shadow:inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)}
.log-box .bright{color:#38bdf8}

.test-result{background:#0f172a;border:1px solid #334155;border-radius:6px;padding:12px;font-size:0.8em;margin-top:16px;min-height:44px;display:flex;align-items:center}
.test-result.success{border-left:4px solid #10b981;color:#10b981}
.test-result.fail{border-left:4px solid #ef4444;color:#ef4444}

footer{margin-top:40px;padding-top:20px;border-top:1px solid #1e293b;font-size:0.8em;color:#64748b;text-align:center}
footer a{color:#38bdf8;text-decoration:none;transition:color 0.2s}
footer a:hover{color:#7dd3fc;text-decoration:underline}

.matrix-rain{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.03;pointer-events:none}

.loading{opacity:0.5;pointer-events:none}

@media(max-width:768px){.panel-grid{grid-template-columns:1fr}}

.status-bar{display:flex;gap:20px;font-size:0.85em;color:#94a3b8;margin-bottom:24px;flex-wrap:wrap;background:#1e293b;padding:12px 16px;border-radius:8px;border:1px solid #334155}
.status-bar span{display:flex;align-items:center;gap:6px}

.toast{position:fixed;bottom:24px;right:24px;background:#1e293b;border-left:4px solid #38bdf8;border-radius:6px;padding:12px 20px;font-size:0.85em;color:#f8fafc;z-index:999;max-width:400px;box-shadow:0 10px 15px -3px rgba(0, 0, 0, 0.1);opacity:0;transform:translateY(20px);transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1)}
.toast.show{opacity:1;transform:translateY(0)}

.confirm-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15, 23, 42, 0.85);backdrop-filter:blur(4px);z-index:1000;justify-content:center;align-items:center}
.confirm-overlay.show{display:flex;animation:fadeIn 0.2s ease-out}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.confirm-dialog{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:32px;max-width:450px;width:90%;text-align:center;box-shadow:0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)}
.confirm-dialog p{margin-bottom:24px;font-size:0.95em;color:#cbd5e1;line-height:1.5}
.confirm-dialog .btn-group{display:flex;gap:16px;justify-content:center}
</style>"""

# Replace the style block
pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_content = pattern.sub(new_css, content)

# Change the matrix rain color to match the theme (indigo/blue instead of green)
new_content = new_content.replace("ctx.fillStyle='#0f0';", "ctx.fillStyle='#6366f1';") # Indigo for matrix rain

with open('panel.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("CSS updated successfully.")
