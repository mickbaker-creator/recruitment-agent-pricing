import base64, gzip, re

# ── Read source HTML
with open('sandbox-recrutiment-pricing.html', 'r') as f:
    html = f.read()

# ── Extract & decompress bundle
b64 = re.search(r'<script[^>]*id="wp-rl-app-data"[^>]*>(.*?)</script>', html, re.DOTALL).group(1).strip()
bundle = gzip.decompress(base64.b64decode(b64)).decode('utf-8')

# ── Locate Pricing function boundaries
p_start = bundle.index('function Pricing(')
p_end   = bundle.index('function FAQ(')

# ── New Pricing function ──────────────────────────────────────────────────────
NEW_PRICING = r'''function Pricing({ onStarted }) {
  const [annual, setAnnual] = React.useState(true);

  const plans = [
    {
      id: "Pro 50",  monthly: 249,  credits: 50,  overage: "$10.00",
      personaAvatar: { initials: "SR", bg: "#EFE8FF", fg: "#7C4DFF" },
      personaRole: "Solo Recruiter",
      personaBlurb: "Handles 2–4 roles at a time for a growing company. Needs AI screening without the overhead of a full talent ops team."
    },
    {
      id: "Pro 100", monthly: 449,  credits: 100, overage: "$9.00",  popular: true,
      personaAvatar: { initials: "HM", bg: "#DCFCE7", fg: "#16A34A" },
      personaRole: "HR Manager",
      personaBlurb: "Scaling headcount fast. Runs 8–10 concurrent roles, needs to hit pipeline volume targets without burning out the team."
    },
    {
      id: "Pro 200", monthly: 799,  credits: 200, overage: "$8.00",
      personaAvatar: { initials: "TL", bg: "#FEF9C3", fg: "#CA8A04" },
      personaRole: "Talent Lead",
      personaBlurb: "Runs specialist searches where every shortlist matters. Combines AI screening with deep candidate evaluation across multiple business units."
    },
    {
      id: "Pro 300", monthly: 1199, credits: 300, overage: "$8.00",
      personaAvatar: { initials: "TA", bg: "#FFE4E6", fg: "#E11D48" },
      personaRole: "Head of Talent Acquisition",
      personaBlurb: "Enterprise or RPO environment. High volume, multiple hiring managers, needs consistent process and reporting at scale."
    }
  ];

  const fmt  = n => "$" + Math.round(n).toLocaleString();
  const fmt2 = n => "$" + n.toFixed(2);

  // SVG person icon
  const PersonIcon = () => React.createElement("svg", {
    width: 16, height: 16, viewBox: "0 0 16 16", fill: "none",
    style: { flexShrink: 0, opacity: 0.45, marginTop: 1 }
  },
    React.createElement("circle", { cx: 8, cy: 5.5, r: 3, stroke: "#121214", strokeWidth: 1.4 }),
    React.createElement("path", { d: "M2 14c0-3.314 2.686-6 6-6s6 2.686 6 6", stroke: "#121214", strokeWidth: 1.4, strokeLinecap: "round" })
  );

  return React.createElement("section", {
    id: "pricing",
    style: { background: "#FFFFFF", padding: "96px 50px", fontFamily: "'DM Sans', sans-serif" }
  },
    React.createElement("div", { style: { maxWidth: 1240, margin: "0 auto", textAlign: "center" } },

      // Eyebrow
      React.createElement("div", { style: { fontSize: 11, color: COLORS.accent, letterSpacing: 2, fontWeight: 600 } }, "TRANSPARENT PRICING"),

      // Headline
      React.createElement("h2", {
        style: { fontSize: 52, lineHeight: 1.05, letterSpacing: -1.4, fontWeight: 700, margin: "16px auto 12px", color: COLORS.textDark, maxWidth: 820 }
      }, "Pay for outcomes, ", React.createElement("span", { style: { color: COLORS.accent } }, "not overhead.")),

      // Sub
      React.createElement("p", { style: { fontSize: 16, color: "#3A3A44", margin: 0 } },
        "Credits reset monthly. Use them across any AI touchpoint."),

      // Credit explainer
      React.createElement("div", {
        style: { maxWidth: 620, margin: "24px auto 0", background: "#EFEAFE", border: "1px solid #D9CFFB", borderRadius: 12, padding: "14px 22px", fontSize: 14, color: "#2A1A52", lineHeight: 1.5 }
      },
        React.createElement("strong", { style: { color: COLORS.accent, fontWeight: 700 } }, "1 Credit = 1 AI Interaction."),
        " This includes screening (text/call), a video interview, or an interview using the AI Notetaker."
      ),

      // Toggle
      React.createElement("div", {
        style: { display: "inline-flex", alignItems: "center", background: "#fff", borderRadius: 999, padding: 5, marginTop: 32, border: "1px solid " + COLORS.borderLight, boxShadow: "0 2px 8px rgba(40,5,65,0.04)" }
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
      ),

      // Plan grid
      React.createElement("div", {
        style: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginTop: 36, textAlign: "left" }
      },
        plans.map(p => {
          const monthlyEffective = annual ? p.monthly * 0.8 : p.monthly;
          const perCredit = monthlyEffective / p.credits;

          return React.createElement("div", {
            key: p.id,
            style: {
              background: "#fff",
              border: (p.popular ? 2 : 1) + "px solid " + (p.popular ? COLORS.accent : COLORS.borderLight),
              borderRadius: 16,
              padding: "24px 24px 20px",
              position: "relative",
              display: "flex",
              flexDirection: "column"
            }
          },
            // Popular badge
            p.popular && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "MOST POPULAR"),

            // Plan name + person icon row
            React.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start" } },
              React.createElement("div", { style: { fontSize: 15, fontWeight: 700, color: COLORS.textDark, letterSpacing: 0.2 } }, p.id),
              React.createElement(PersonIcon)
            ),

            // Price
            React.createElement("div", { style: { display: "flex", alignItems: "baseline", gap: 4, marginTop: 10 } },
              React.createElement("span", { style: { fontSize: 38, fontWeight: 700, letterSpacing: -1.4, color: COLORS.textDark } }, fmt(monthlyEffective)),
              React.createElement("span", { style: { fontSize: 13, color: COLORS.textDim } }, "/mo"),
              annual && React.createElement("span", { style: { fontSize: 13, color: COLORS.textDim, textDecoration: "line-through", marginLeft: 6 } }, fmt(p.monthly))
            ),
            React.createElement("div", { style: { fontSize: 12, color: COLORS.textDim, marginTop: 4 } },
              annual
                ? React.createElement(React.Fragment, null, "Billed monthly · ", fmt(monthlyEffective * 12), "/yr")
                : "Billed monthly"
            ),

            // CTA button
            React.createElement("button", {
              onClick: () => onStarted(null),
              style: { marginTop: 16, width: "100%", background: p.popular ? COLORS.accent : "transparent", color: p.popular ? "#fff" : COLORS.accent, border: "1px solid " + COLORS.accent, borderRadius: 10, padding: "12px 18px", fontSize: 13, fontWeight: 700, cursor: "pointer", fontFamily: "inherit" }
            }, "Get started"),

            // Divider
            React.createElement("div", { style: { borderTop: "1px solid " + COLORS.borderLight, margin: "20px 0 16px" } }),

            // Credits + per-credit stats
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

            // Overage
            React.createElement("div", {
              title: "Need more? Extra interactions at " + p.overage + "/credit. No hard cap.",
              style: { display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11, color: COLORS.textDim, cursor: "help", borderBottom: "1px dashed " + COLORS.borderLight, paddingBottom: 1, alignSelf: "flex-start", marginBottom: 20 }
            },
              "Overage ",
              React.createElement("span", { style: { color: COLORS.textDark, fontWeight: 600 } }, p.overage),
              "/credit"
            ),

            // ── Persona section ──────────────────────────────────────────
            React.createElement("div", { style: { borderTop: "1px solid " + COLORS.borderLight, paddingTop: 16, marginTop: "auto" } },
              // Avatar circle + role
              React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 10 } },
                React.createElement("div", {
                  style: {
                    width: 36, height: 36, borderRadius: "50%",
                    background: p.personaAvatar.bg,
                    color: p.personaAvatar.fg,
                    fontSize: 12, fontWeight: 700,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    flexShrink: 0,
                    border: "1.5px solid " + p.personaAvatar.fg + "33"
                  }
                }, p.personaAvatar.initials),
                React.createElement("div", { style: { fontSize: 13, fontWeight: 700, color: COLORS.textDark, lineHeight: 1.3 } }, p.personaRole)
              ),
              // Description blurb
              React.createElement("p", {
                style: { fontSize: 12, color: COLORS.textDim, lineHeight: 1.55, margin: 0 }
              }, p.personaBlurb)
            )
          );
        })
      ),

      // High Volume CTA
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

      // Legal footnote
      React.createElement("p", {
        style: { marginTop: 24, textAlign: "center", fontSize: 12, color: "#8A8A95", lineHeight: 1.5 }
      }, "All prices AUD ex. GST · Monthly plans billed monthly, cancel anytime · Annual plans billed monthly on a 12-month contract · Credits reset monthly, unused credits do not roll over. Overage billed automatically, no hard cap · No Employment Hero HR or payroll subscription required.")
    )
  );
}

'''

# ── Splice into bundle
new_bundle = bundle[:p_start] + NEW_PRICING + bundle[p_end:]

# ── Recompress
new_b64 = base64.b64encode(gzip.compress(new_bundle.encode('utf-8'), compresslevel=6)).decode('ascii')

# ── Inject back into HTML (replace only the script body, keep attributes)
new_html = re.sub(
    r'(<script[^>]*id="wp-rl-app-data"[^>]*>)(.*?)(</script>)',
    lambda m: m.group(1) + new_b64 + m.group(3),
    html,
    flags=re.DOTALL
)

out = 'variant-1-personas.html'
with open(out, 'w') as f:
    f.write(new_html)

print(f"Written: {out}  ({len(new_html):,} bytes)")
