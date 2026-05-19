import base64, gzip, re

with open('sandbox-recrutiment-pricing.html', 'r') as f:
    html = f.read()

b64 = re.search(r'<script[^>]*id="wp-rl-app-data"[^>]*>(.*?)</script>', html, re.DOTALL).group(1).strip()
bundle = gzip.decompress(base64.b64decode(b64)).decode('utf-8')

p_start = bundle.index('function Pricing(')
p_end   = bundle.index('function FAQ(')

NEW_PRICING = r'''function Pricing({ onStarted }) {
  const [annual,   setAnnual]   = React.useState(true);
  const [selected, setSelected] = React.useState(null);

  const situations = [
    { planId: "Pro 50",  label: "We fill a handful of roles each month",          hint: "Typically 1–5 hires/mo" },
    { planId: "Pro 100", label: "We’re scaling up and hiring pretty often",    hint: "Typically 5–12 hires/mo" },
    { planId: "Pro 200", label: "Hiring spans multiple teams or clients",           hint: "Typically 12–25 hires/mo" },
    { planId: "Pro 300", label: "Volume hiring is core to how we operate",          hint: "Typically 25+ hires/mo" }
  ];

  const plans = [
    { id: "Pro 50",  monthly: 249,  credits: 50,  overage: "$10.00" },
    { id: "Pro 100", monthly: 449,  credits: 100, overage: "$9.00",  popular: true },
    { id: "Pro 200", monthly: 799,  credits: 200, overage: "$8.00"  },
    { id: "Pro 300", monthly: 1199, credits: 300, overage: "$8.00"  }
  ];

  const fmt  = n => "$" + Math.round(n).toLocaleString();
  const fmt2 = n => "$" + n.toFixed(2);

  return React.createElement("section", {
    id: "pricing",
    style: { background: "#FFFFFF", padding: "96px 50px", fontFamily: "'DM Sans', sans-serif" }
  },
    React.createElement("div", { style: { maxWidth: 1240, margin: "0 auto" } },

      // ── Header
      React.createElement("div", { style: { textAlign: "center", marginBottom: 40 } },
        React.createElement("div", { style: { fontSize: 11, color: COLORS.accent, letterSpacing: 2, fontWeight: 600 } }, "TRANSPARENT PRICING"),
        React.createElement("h2", {
          style: { fontSize: 52, lineHeight: 1.05, letterSpacing: -1.4, fontWeight: 700, margin: "16px auto 12px", color: COLORS.textDark, maxWidth: 820 }
        }, "Pay for outcomes, ", React.createElement("span", { style: { color: COLORS.accent } }, "not overhead.")),
        React.createElement("p", { style: { fontSize: 16, color: "#3A3A44", margin: 0 } },
          "Credits reset monthly. Use them across any AI touchpoint.")
      ),

      // ── Situation selector
      React.createElement("div", { style: { textAlign: "center", marginBottom: 44 } },
        React.createElement("p", {
          style: { fontSize: 13, fontWeight: 600, color: COLORS.textDim, letterSpacing: 0.3, marginBottom: 14 }
        }, "Which best describes your hiring right now?"),
        React.createElement("div", {
          style: { display: "inline-flex", flexWrap: "wrap", gap: 10, justifyContent: "center", maxWidth: 900 }
        },
          situations.map((s, i) => {
            const isActive = selected === s.planId;
            return React.createElement("button", {
              key: s.planId,
              onClick: () => setSelected(isActive ? null : s.planId),
              style: {
                border: "1.5px solid " + (isActive ? COLORS.accent : "#E2DDFB"),
                borderRadius: 999,
                padding: "11px 22px",
                background: isActive ? COLORS.accent : "#FDFAFF",
                color: isActive ? "#fff" : "#3A3057",
                fontSize: 13,
                fontWeight: isActive ? 700 : 500,
                cursor: "pointer",
                fontFamily: "inherit",
                display: "inline-flex",
                alignItems: "center",
                gap: 8,
                transition: "all 0.18s",
                boxShadow: isActive ? "0 2px 12px rgba(124,77,255,0.25)" : "none"
              }
            },
              // Numbered indicator
              React.createElement("span", {
                style: {
                  width: 20, height: 20, borderRadius: "50%",
                  background: isActive ? "rgba(255,255,255,0.25)" : "#EDE9FC",
                  color: isActive ? "#fff" : COLORS.accent,
                  fontSize: 10, fontWeight: 700,
                  display: "inline-flex", alignItems: "center", justifyContent: "center",
                  flexShrink: 0
                }
              }, i + 1),
              s.label
            );
          })
        ),
        // Hint line — shows the hint for the selected chip
        React.createElement("div", {
          style: { marginTop: 12, fontSize: 12, color: COLORS.textDim, minHeight: 18, transition: "opacity 0.2s", opacity: selected ? 1 : 0 }
        },
          selected
            ? (situations.find(s => s.planId === selected) || {}).hint
            : " "
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
          const isMatch    = selected === p.id;
          const hasSel     = selected !== null;
          const monthlyEff = annual ? p.monthly * 0.8 : p.monthly;
          const perCredit  = monthlyEff / p.credits;
          const dimmed     = hasSel && !isMatch;

          return React.createElement("div", {
            key: p.id,
            style: {
              background: isMatch ? "#FDFAFF" : "#fff",
              border: (isMatch ? 2 : 1) + "px solid " + (isMatch ? COLORS.accent : COLORS.borderLight),
              borderRadius: 16,
              padding: 24,
              position: "relative",
              display: "flex",
              flexDirection: "column",
              transition: "all 0.22s",
              opacity: dimmed ? 0.45 : 1,
              boxShadow: isMatch ? "0 0 0 4px rgba(124,77,255,0.10)" : "none",
              transform: isMatch ? "translateY(-3px)" : "none"
            }
          },
            // Badge: "RECOMMENDED FOR YOU" when matched, else "MOST POPULAR" on Pro 100 with no selection
            isMatch && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 14px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "RECOMMENDED FOR YOU"),
            !hasSel && p.popular && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 14px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
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
                ? React.createElement(React.Fragment, null, "Billed monthly \xB7 ", fmt(monthlyEff * 12), "/yr")
                : "Billed monthly"
            ),

            // Divider + stats
            React.createElement("div", { style: { marginTop: 18, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, padding: "14px 0", borderTop: "1px solid " + COLORS.borderLight, borderBottom: "1px solid " + COLORS.borderLight } },
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

            // Overage
            React.createElement("div", {
              title: "Need more than " + p.credits + " credits? Extra interactions at " + p.overage + "/credit. No hard cap.",
              style: { marginTop: 12, display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11, color: COLORS.textDim, cursor: "help", borderBottom: "1px dashed " + COLORS.borderLight, paddingBottom: 1, alignSelf: "flex-start" }
            },
              "Overage ",
              React.createElement("span", { style: { color: COLORS.textDark, fontWeight: 600 } }, p.overage),
              "/credit"
            ),

            // CTA
            React.createElement("button", {
              onClick: () => onStarted(null),
              style: { marginTop: 18, width: "100%", background: isMatch ? COLORS.accent : "transparent", color: isMatch ? "#fff" : COLORS.accent, border: "1px solid " + COLORS.accent, borderRadius: 10, padding: "12px 18px", fontSize: 13, fontWeight: 700, cursor: "pointer", fontFamily: "inherit", transition: "all 0.18s" }
            }, "Get started")
          );
        })
      ),

      // ── High volume CTA
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

out = 'variant-3-situation-chips.html'
with open(out, 'w') as f:
    f.write(new_html)
print(f"Written: {out}  ({len(new_html):,} bytes)")
