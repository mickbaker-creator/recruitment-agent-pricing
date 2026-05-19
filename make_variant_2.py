import base64, gzip, re

with open('sandbox-recrutiment-pricing.html', 'r') as f:
    html = f.read()

b64 = re.search(r'<script[^>]*id="wp-rl-app-data"[^>]*>(.*?)</script>', html, re.DOTALL).group(1).strip()
bundle = gzip.decompress(base64.b64decode(b64)).decode('utf-8')

p_start = bundle.index('function Pricing(')
p_end   = bundle.index('function FAQ(')

NEW_PRICING = r'''function Pricing({ onStarted }) {
  const [annual,           setAnnual]           = React.useState(true);
  const [rolesPerQtr,      setRolesPerQtr]      = React.useState(15);
  const [candidatesPerRole,setCandidatesPerRole] = React.useState(5);
  const [steps, setSteps] = React.useState({ screening: true, video: true, notetaker: false });

  const plans = [
    { id: "Pro 50",  monthly: 249,  credits: 50,  overage: "$10.00" },
    { id: "Pro 100", monthly: 449,  credits: 100, overage: "$9.00",  popular: true },
    { id: "Pro 200", monthly: 799,  credits: 200, overage: "$8.00"  },
    { id: "Pro 300", monthly: 1199, credits: 300, overage: "$8.00"  }
  ];

  const stepDefs = [
    { key: "screening",  label: "AI Screening Call",  desc: "Text or phone screen"  },
    { key: "video",      label: "Video Interview",    desc: "Async or live AI panel" },
    { key: "notetaker",  label: "AI Notetaker",       desc: "Structured human interview" }
  ];

  const toggleStep = key => setSteps(s => ({ ...s, [key]: !s[key] }));

  // ── Credit estimate
  const activeSteps   = stepDefs.filter(s => steps[s.key]).length || 1;
  const rolesPerMonth = rolesPerQtr / 3;
  const creditsEst    = Math.ceil(rolesPerMonth * candidatesPerRole * activeSteps);

  // First plan with enough credits; fall back to largest
  const recommended = plans.find(p => p.credits >= creditsEst) || plans[plans.length - 1];
  const isOverAll   = creditsEst > plans[plans.length - 1].credits;

  const fmt  = n => "$" + Math.round(n).toLocaleString();
  const fmt2 = n => "$" + n.toFixed(2);

  // ── Slider component
  const Slider = ({ label, value, min, max, step, onChange, format }) =>
    React.createElement("div", { style: { flex: 1 } },
      React.createElement("div", {
        style: { display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }
      },
        React.createElement("span", { style: { fontSize: 12, fontWeight: 600, color: "#3A3A44" } }, label),
        React.createElement("span", { style: { fontSize: 18, fontWeight: 700, color: COLORS.textDark, letterSpacing: -0.5 } },
          format ? format(value) : value
        )
      ),
      React.createElement("input", {
        type: "range", min, max, step, value,
        onChange: e => onChange(Number(e.target.value)),
        style: { width: "100%", accentColor: COLORS.accent, cursor: "pointer" }
      }),
      React.createElement("div", { style: { display: "flex", justifyContent: "space-between", marginTop: 3 } },
        React.createElement("span", { style: { fontSize: 10, color: COLORS.textDim } }, min),
        React.createElement("span", { style: { fontSize: 10, color: COLORS.textDim } }, max)
      )
    );

  return React.createElement("section", {
    id: "pricing",
    style: { background: "#FFFFFF", padding: "96px 50px", fontFamily: "'DM Sans', sans-serif" }
  },
    React.createElement("div", { style: { maxWidth: 1240, margin: "0 auto" } },

      // ── Header (centred)
      React.createElement("div", { style: { textAlign: "center", marginBottom: 48 } },
        React.createElement("div", { style: { fontSize: 11, color: COLORS.accent, letterSpacing: 2, fontWeight: 600 } }, "TRANSPARENT PRICING"),
        React.createElement("h2", {
          style: { fontSize: 52, lineHeight: 1.05, letterSpacing: -1.4, fontWeight: 700, margin: "16px auto 12px", color: COLORS.textDark, maxWidth: 820 }
        }, "Pay for outcomes, ", React.createElement("span", { style: { color: COLORS.accent } }, "not overhead.")),
        React.createElement("p", { style: { fontSize: 16, color: "#3A3A44", margin: 0 } },
          "Credits reset monthly. Use them across any AI touchpoint.")
      ),

      // ── Calculator panel
      React.createElement("div", {
        style: { background: "#F9F5FF", border: "1px solid #E0D6FC", borderRadius: 20, padding: "32px 36px", marginBottom: 36 }
      },
        React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 24 } },
          React.createElement("div", {
            style: { width: 28, height: 28, borderRadius: 8, background: COLORS.accent, display: "flex", alignItems: "center", justifyContent: "center" }
          },
            React.createElement("svg", { width: 14, height: 14, viewBox: "0 0 14 14", fill: "none" },
              React.createElement("rect", { x: 1, y: 1, width: 4, height: 4, rx: 1, fill: "#fff" }),
              React.createElement("rect", { x: 1, y: 7, width: 4, height: 4, rx: 1, fill: "#fff" }),
              React.createElement("rect", { x: 7, y: 1, width: 4, height: 4, rx: 1, fill: "#fff" }),
              React.createElement("rect", { x: 7, y: 7, width: 4, height: 4, rx: 1, fill: "#fff" })
            )
          ),
          React.createElement("div", null,
            React.createElement("div", { style: { fontSize: 14, fontWeight: 700, color: COLORS.textDark } }, "Credit estimator"),
            React.createElement("div", { style: { fontSize: 12, color: COLORS.textDim } }, "Dial in your hiring context — we'll show the right plan")
          )
        ),

        // Sliders row
        React.createElement("div", { style: { display: "flex", gap: 32, marginBottom: 24 } },
          React.createElement(Slider, {
            label: "Roles per quarter", value: rolesPerQtr,
            min: 1, max: 100, step: 1,
            onChange: setRolesPerQtr
          }),
          React.createElement(Slider, {
            label: "Candidates per role", value: candidatesPerRole,
            min: 1, max: 20, step: 1,
            onChange: setCandidatesPerRole,
            format: n => n + " candidates"
          })
        ),

        // Steps row + result
        React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" } },
          // Step checkboxes
          React.createElement("div", { style: { flex: 1 } },
            React.createElement("div", { style: { fontSize: 12, fontWeight: 600, color: "#3A3A44", marginBottom: 10 } }, "AI steps per candidate"),
            React.createElement("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" } },
              stepDefs.map(s =>
                React.createElement("label", {
                  key: s.key,
                  style: { display: "flex", alignItems: "center", gap: 7, cursor: "pointer", background: steps[s.key] ? COLORS.accentSoft : "#fff", border: "1px solid " + (steps[s.key] ? COLORS.accent : COLORS.borderLight), borderRadius: 8, padding: "7px 12px", fontSize: 12, fontWeight: 600, color: steps[s.key] ? COLORS.accent : "#6A6A74", userSelect: "none", transition: "all 0.15s" }
                },
                  React.createElement("input", {
                    type: "checkbox", checked: steps[s.key],
                    onChange: () => toggleStep(s.key),
                    style: { accentColor: COLORS.accent, width: 13, height: 13 }
                  }),
                  React.createElement("span", null, s.label),
                  React.createElement("span", { style: { fontWeight: 400, opacity: 0.65 } }, "· " + s.desc)
                )
              )
            )
          ),

          // Result box
          React.createElement("div", {
            style: { background: "#fff", border: "2px solid " + (isOverAll ? "#E11D48" : COLORS.accent), borderRadius: 14, padding: "16px 24px", minWidth: 220, textAlign: "center", flexShrink: 0 }
          },
            React.createElement("div", { style: { fontSize: 11, color: isOverAll ? "#E11D48" : COLORS.accent, fontWeight: 700, letterSpacing: 1.5, marginBottom: 6 } },
              isOverAll ? "CUSTOM VOLUME" : "YOUR ESTIMATE"
            ),
            React.createElement("div", { style: { fontSize: 40, fontWeight: 700, letterSpacing: -1.5, color: COLORS.textDark, lineHeight: 1 } },
              creditsEst
            ),
            React.createElement("div", { style: { fontSize: 12, color: COLORS.textDim, marginTop: 4 } }, "credits / month"),
            React.createElement("div", {
              style: { marginTop: 10, fontSize: 11, color: "#5A5A64", background: "#F4F1FA", borderRadius: 6, padding: "4px 8px", lineHeight: 1.4 }
            },
              Math.round(rolesPerMonth * 10) / 10, " roles/mo × ", candidatesPerRole, " candidates × ", activeSteps, " step", activeSteps !== 1 ? "s" : ""
            ),
            !isOverAll && React.createElement("div", { style: { marginTop: 8, fontSize: 12, fontWeight: 700, color: COLORS.accent } },
              "→ ", recommended.id, " recommended"
            ),
            isOverAll && React.createElement("div", { style: { marginTop: 8, fontSize: 12, fontWeight: 700, color: "#E11D48" } },
              "→ Talk to sales"
            )
          )
        )
      ),

      // ── Toggle
      React.createElement("div", { style: { textAlign: "center", marginBottom: 28 } },
        React.createElement("div", {
          style: { display: "inline-flex", alignItems: "center", background: "#fff", borderRadius: 999, padding: 5, border: "1px solid " + COLORS.borderLight, boxShadow: "0 2px 8px rgba(40,5,65,0.04)" }
        },
          React.createElement("button", {
            onClick: () => setAnnual(false),
            style: { border: 0, cursor: "pointer", fontFamily: "inherit", padding: "9px 22px", borderRadius: 999, fontSize: 13, fontWeight: 700, background: !annual ? "#1A0A2E" : "transparent", color: !annual ? "#fff" : "#6A6A74", transition: "all 0.18s" }
          }, "Monthly"),
          React.createElement("button", {
            onClick: () => setAnnual(true),
            style: { border: 0, cursor: "pointer", fontFamily: "inherit", padding: "9px 18px", borderRadius: 999, fontSize: 13, fontWeight: 700, background: annual ? "#1A0A2E" : "transparent", color: annual ? "#fff" : "#6A6A74", display: "inline-flex", alignItems: "center", gap: 8, transition: "all 0.18s" }
          },
            "Annual",
            React.createElement("span", { style: { fontSize: 10, fontWeight: 700, letterSpacing: 0.4, padding: "3px 8px", borderRadius: 999, background: "#94E022", color: "#121214" } }, "Save 20%")
          )
        )
      ),

      // ── Plan cards
      React.createElement("div", {
        style: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, textAlign: "left" }
      },
        plans.map(p => {
          const isBestFit      = !isOverAll && p.id === recommended.id;
          const monthlyEff     = annual ? p.monthly * 0.8 : p.monthly;
          const perCredit      = monthlyEff / p.credits;
          const coverageRatio  = Math.min(p.credits / creditsEst, 1);
          const barColor       = isBestFit ? COLORS.accent : (p.credits < creditsEst ? "#E11D48" : COLORS.borderLight);

          return React.createElement("div", {
            key: p.id,
            style: {
              background: isBestFit ? "#FDFAFF" : "#fff",
              border: (isBestFit ? 2 : 1) + "px solid " + (isBestFit ? COLORS.accent : COLORS.borderLight),
              borderRadius: 16, padding: 24, position: "relative",
              display: "flex", flexDirection: "column",
              transition: "border-color 0.25s, box-shadow 0.25s",
              boxShadow: isBestFit ? "0 0 0 4px rgba(124,77,255,0.10)" : "none"
            }
          },
            // Best fit badge (replaces popular badge when calculator is used)
            isBestFit && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "BEST FIT FOR YOU"),

            !isBestFit && p.popular && !isOverAll && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: "#E4E4E7", color: "#6A6A74", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "MOST POPULAR"),

            !isBestFit && p.popular && isOverAll && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "MOST POPULAR"),

            // Plan name
            React.createElement("div", { style: { fontSize: 15, fontWeight: 700, color: COLORS.textDark, letterSpacing: 0.2 } }, p.id),

            // Price
            React.createElement("div", { style: { display: "flex", alignItems: "baseline", gap: 4, marginTop: 10 } },
              React.createElement("span", { style: { fontSize: 38, fontWeight: 700, letterSpacing: -1.4, color: COLORS.textDark } }, fmt(monthlyEff)),
              React.createElement("span", { style: { fontSize: 13, color: COLORS.textDim } }, "/mo"),
              annual && React.createElement("span", { style: { fontSize: 13, color: COLORS.textDim, textDecoration: "line-through", marginLeft: 6 } }, fmt(p.monthly))
            ),
            React.createElement("div", { style: { fontSize: 12, color: COLORS.textDim, marginTop: 4 } },
              annual
                ? React.createElement(React.Fragment, null, "Billed monthly · ", fmt(monthlyEff * 12), "/yr")
                : "Billed monthly"
            ),

            // Divider
            React.createElement("div", { style: { borderTop: "1px solid " + COLORS.borderLight, margin: "18px 0 14px" } }),

            // Credits + per credit
            React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 14 } },
              React.createElement("div", null,
                React.createElement("div", { style: { fontSize: 10, color: COLORS.textDim, letterSpacing: 1, fontWeight: 600 } }, "CREDITS"),
                React.createElement("div", { style: { fontSize: 22, fontWeight: 700, letterSpacing: -0.5, color: COLORS.textDark, marginTop: 2 } },
                  p.credits,
                  React.createElement("span", { style: { fontSize: 12, fontWeight: 500, color: COLORS.textDim, marginLeft: 3 } }, "/mo")
                )
              ),
              React.createElement("div", null,
                React.createElement("div", { style: { fontSize: 10, color: COLORS.textDim, letterSpacing: 1, fontWeight: 600 } }, "PER CREDIT"),
                React.createElement("div", { style: { fontSize: 22, fontWeight: 700, letterSpacing: -0.5, color: COLORS.accent, marginTop: 2 } }, fmt2(perCredit))
              )
            ),

            // Coverage bar — shows how well this plan covers the user's estimate
            creditsEst > 0 && React.createElement("div", { style: { marginBottom: 14 } },
              React.createElement("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 4 } },
                React.createElement("span", { style: { fontSize: 10, color: COLORS.textDim, fontWeight: 600, letterSpacing: 1 } }, "COVERS YOUR ESTIMATE"),
                React.createElement("span", { style: { fontSize: 10, fontWeight: 700, color: p.credits < creditsEst ? "#E11D48" : COLORS.accent } },
                  p.credits < creditsEst
                    ? p.credits + "/" + creditsEst + " — needs overage"
                    : p.credits >= creditsEst ? "✓ fits" : ""
                )
              ),
              React.createElement("div", { style: { height: 4, background: "#F0EDFB", borderRadius: 99 } },
                React.createElement("div", {
                  style: { height: 4, borderRadius: 99, background: barColor, width: (Math.min(coverageRatio, 1) * 100) + "%", transition: "width 0.3s, background 0.3s" }
                })
              )
            ),

            // Overage
            React.createElement("div", {
              title: "Extra interactions at " + p.overage + "/credit — no hard cap.",
              style: { display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11, color: COLORS.textDim, cursor: "help", borderBottom: "1px dashed " + COLORS.borderLight, paddingBottom: 1, alignSelf: "flex-start", marginBottom: 18 }
            },
              "Overage ",
              React.createElement("span", { style: { color: COLORS.textDark, fontWeight: 600 } }, p.overage),
              "/credit"
            ),

            // CTA
            React.createElement("button", {
              onClick: () => onStarted(null),
              style: { marginTop: "auto", width: "100%", background: isBestFit ? COLORS.accent : "transparent", color: isBestFit ? "#fff" : COLORS.accent, border: "1px solid " + COLORS.accent, borderRadius: 10, padding: "12px 18px", fontSize: 13, fontWeight: 700, cursor: "pointer", fontFamily: "inherit", transition: "all 0.15s" }
            }, isBestFit ? "Get started — " + p.id : "Get started")
          );
        })
      ),

      // ── High Volume CTA
      React.createElement("div", {
        style: { marginTop: 56, background: "#F9F5FF", borderRadius: 24, padding: "36px 48px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 32, position: "relative", overflow: "hidden" }
      },
        React.createElement("div", { style: { position: "absolute", right: -120, top: "50%", transform: "translateY(-50%)", width: 360, height: 360, borderRadius: "50%", background: "radial-gradient(circle, rgba(199,245,98,0.10) 0%, rgba(199,245,98,0) 65%)", pointerEvents: "none" } }),
        React.createElement("div", { style: { position: "relative", zIndex: 1, flex: 1 } },
          React.createElement("span", { style: { display: "inline-block", background: "#7622D7", color: "#FFFFFF", fontSize: 11, fontWeight: 700, letterSpacing: 1, padding: "5px 10px", borderRadius: 6, marginBottom: 18 } }, "HIGH VOLUME"),
          React.createElement("h3", { style: { fontSize: 32, lineHeight: 1.15, fontWeight: 600, color: "#121214", margin: "0 0 8px", letterSpacing: -0.5 } }, "More than 300 interviews a month?"),
          React.createElement("p", { style: { fontSize: 15, color: "rgba(18,18,20,0.6)", margin: 0, lineHeight: 1.5 } }, "Get a custom plan tailored to your hiring volume.")
        ),
        React.createElement("button", {
          type: "button", onClick: () => onStarted(null),
          style: { position: "relative", zIndex: 1, flexShrink: 0, background: "#7622D7", color: "#FFFFFF", border: "none", borderRadius: 999, padding: "14px 24px", fontSize: 14, fontWeight: 700, cursor: "pointer", fontFamily: "inherit", display: "inline-flex", alignItems: "center", gap: 8 }
        }, "Speak to sales ", React.createElement("span", { "aria-hidden": "true" }, "→"))
      ),

      // Legal
      React.createElement("p", {
        style: { marginTop: 24, textAlign: "center", fontSize: 12, color: "#8A8A95", lineHeight: 1.5 }
      }, "All prices AUD ex. GST \xB7 Monthly plans billed monthly, cancel anytime \xB7 Annual plans billed monthly on a 12-month contract \xB7 Credits reset monthly, unused credits do not roll over. Overage billed automatically, no hard cap \xB7 No Employment Hero HR or payroll subscription required.")
    )
  );
}

'''

new_bundle = bundle[:p_start] + NEW_PRICING + bundle[p_end:]
new_b64 = base64.b64encode(gzip.compress(new_bundle.encode('utf-8'), compresslevel=6)).decode('ascii')

new_html = re.sub(
    r'(<script[^>]*id="wp-rl-app-data"[^>]*>)(.*?)(</script>)',
    lambda m: m.group(1) + new_b64 + m.group(3),
    html, flags=re.DOTALL
)

out = 'variant-2-calculator.html'
with open(out, 'w') as f:
    f.write(new_html)

print(f"Written: {out}  ({len(new_html):,} bytes)")
