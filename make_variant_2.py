import base64, gzip, re

with open('sandbox-recrutiment-pricing.html', 'r') as f:
    html = f.read()

b64 = re.search(r'<script[^>]*id="wp-rl-app-data"[^>]*>(.*?)</script>', html, re.DOTALL).group(1).strip()
bundle = gzip.decompress(base64.b64decode(b64)).decode('utf-8')

p_start = bundle.index('function Pricing(')
p_end   = bundle.index('function FAQ(')

NEW_PRICING = r'''function Pricing({ onStarted }) {
  const [annual,       setAnnual]      = React.useState(true);
  const [roles,        setRoles]       = React.useState(8);
  const [aiScreens,    setAiScreens]   = React.useState(15);
  const [videoInt,     setVideoInt]    = React.useState(6);
  const [notetaker,    setNotetaker]   = React.useState(2);
  const [useScreens,   setUseScreens]  = React.useState(true);
  const [useVideo,     setUseVideo]    = React.useState(true);
  const [useNote,      setUseNote]     = React.useState(false);

  const plans = [
    { id: "Pro 50",  monthly: 249,  credits: 50,  overage: "$10.00" },
    { id: "Pro 100", monthly: 449,  credits: 100, overage: "$9.00",  popular: true },
    { id: "Pro 200", monthly: 799,  credits: 200, overage: "$8.00"  },
    { id: "Pro 300", monthly: 1199, credits: 300, overage: "$8.00"  }
  ];

  // 1 credit = 1 AI interaction. Interactions per role = sum of active stage volumes.
  const screensCredits   = useScreens ? aiScreens : 0;
  const videoCredits     = useVideo   ? videoInt  : 0;
  const notetakerCredits = useNote    ? notetaker : 0;
  const interactionsPerRole = screensCredits + videoCredits + notetakerCredits;
  const creditsEst = roles * interactionsPerRole;

  const recommended = plans.find(p => p.credits >= creditsEst) || plans[plans.length - 1];
  const isOverAll   = creditsEst > plans[plans.length - 1].credits;

  const fmt  = n => "$" + Math.round(n).toLocaleString();
  const fmt2 = n => "$" + n.toFixed(2);

  // ── Stepper — plain helper fn (not a component, avoids re-mount bugs)
  const mkStepper = (value, setter, min, max) =>
    React.createElement("div", { style: { display: "flex", alignItems: "center" } },
      React.createElement("button", {
        onClick: () => setter(Math.max(min, value - 1)),
        style: { width: 30, height: 30, borderRadius: "8px 0 0 8px", border: "1px solid #DDD6FE", borderRight: 0, background: "#F5F3FF", cursor: "pointer", fontFamily: "inherit", fontSize: 18, lineHeight: 1, color: COLORS.accent, fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center" }
      }, "−"),
      React.createElement("div", {
        style: { minWidth: 44, height: 30, border: "1px solid #DDD6FE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, fontWeight: 700, color: COLORS.textDark, background: "#fff", letterSpacing: -0.3 }
      }, value),
      React.createElement("button", {
        onClick: () => setter(Math.min(max, value + 1)),
        style: { width: 30, height: 30, borderRadius: "0 8px 8px 0", border: "1px solid #DDD6FE", borderLeft: 0, background: "#F5F3FF", cursor: "pointer", fontFamily: "inherit", fontSize: 18, lineHeight: 1, color: COLORS.accent, fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center" }
      }, "+")
    );

  // ── Toggle switch (CSS-only via inline style trick)
  const mkToggle = (on, setOn, id) =>
    React.createElement("label", {
      htmlFor: id,
      style: { position: "relative", display: "inline-block", width: 36, height: 20, cursor: "pointer", flexShrink: 0 }
    },
      React.createElement("input", {
        id, type: "checkbox", checked: on, onChange: () => setOn(!on),
        style: { opacity: 0, width: 0, height: 0, position: "absolute" }
      }),
      React.createElement("span", {
        style: {
          position: "absolute", inset: 0,
          background: on ? COLORS.accent : "#D1D5DB",
          borderRadius: 999,
          transition: "background 0.2s"
        }
      }),
      React.createElement("span", {
        style: {
          position: "absolute",
          top: 3, left: on ? 19 : 3,
          width: 14, height: 14,
          background: "#fff",
          borderRadius: "50%",
          transition: "left 0.2s",
          boxShadow: "0 1px 3px rgba(0,0,0,0.2)"
        }
      })
    );

  // ── Funnel stage row
  const stageRow = (icon, label, sub, enabled, setEnabled, toggleId, value, setter, min, max, creditCount) =>
    React.createElement("div", {
      style: {
        display: "flex", alignItems: "center", gap: 14,
        padding: "14px 16px", borderRadius: 12,
        background: enabled ? "#FDFAFF" : "#FAFAFA",
        border: "1px solid " + (enabled ? "#E0D6FC" : "#EBEBEB"),
        transition: "all 0.2s", opacity: enabled ? 1 : 0.55
      }
    },
      // Icon
      React.createElement("div", {
        style: { width: 36, height: 36, borderRadius: 10, background: enabled ? COLORS.accentSoft : "#F0F0F0", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17, flexShrink: 0, transition: "background 0.2s" }
      }, icon),
      // Label + sub
      React.createElement("div", { style: { flex: 1, minWidth: 0 } },
        React.createElement("div", { style: { fontSize: 13, fontWeight: 700, color: COLORS.textDark } }, label),
        React.createElement("div", { style: { fontSize: 11, color: COLORS.textDim, marginTop: 1 } }, sub)
      ),
      // Stepper
      React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6 } },
        mkStepper(value, setter, min, max),
        React.createElement("span", { style: { fontSize: 11, color: COLORS.textDim, width: 72, textAlign: "left" } }, "per role")
      ),
      // Credit count badge
      React.createElement("div", {
        style: { minWidth: 80, textAlign: "right" }
      },
        enabled
          ? React.createElement("div", null,
              React.createElement("span", { style: { fontSize: 17, fontWeight: 700, color: COLORS.accent, letterSpacing: -0.5 } }, creditCount),
              React.createElement("span", { style: { fontSize: 11, color: COLORS.textDim, marginLeft: 3 } }, "credits")
            )
          : React.createElement("span", { style: { fontSize: 12, color: "#CCC" } }, "—")
      ),
      // Toggle
      mkToggle(enabled, setEnabled, toggleId)
    );

  return React.createElement("section", {
    id: "pricing",
    style: { background: "#FFFFFF", padding: "96px 50px", fontFamily: "'DM Sans', sans-serif" }
  },
    React.createElement("div", { style: { maxWidth: 1240, margin: "0 auto" } },

      // ── Section header
      React.createElement("div", { style: { textAlign: "center", marginBottom: 52 } },
        React.createElement("div", { style: { fontSize: 11, color: COLORS.accent, letterSpacing: 2, fontWeight: 600 } }, "TRANSPARENT PRICING"),
        React.createElement("h2", {
          style: { fontSize: 52, lineHeight: 1.05, letterSpacing: -1.4, fontWeight: 700, margin: "16px auto 12px", color: COLORS.textDark, maxWidth: 820 }
        }, "Pay for outcomes, ", React.createElement("span", { style: { color: COLORS.accent } }, "not overhead.")),
        React.createElement("p", { style: { fontSize: 16, color: "#3A3A44", margin: "0 auto", maxWidth: 520 } },
          "Every credit is one AI interaction — a screening call, text exchange, video interview, or notetaker session.")
      ),

      // ── Calculator card
      React.createElement("div", {
        style: { display: "grid", gridTemplateColumns: "1fr 300px", gap: 0, background: "#fff", border: "1px solid #E8E3F6", borderRadius: 20, overflow: "hidden", marginBottom: 36, boxShadow: "0 2px 16px rgba(100,60,200,0.06)" }
      },

        // Left: inputs
        React.createElement("div", { style: { padding: "32px 36px", borderRight: "1px solid #F0ECFB" } },
          React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, marginBottom: 28 } },
            React.createElement("div", {
              style: { width: 36, height: 36, borderRadius: 10, background: COLORS.accentSoft, display: "flex", alignItems: "center", justifyContent: "center" }
            },
              React.createElement("svg", { width: 18, height: 18, viewBox: "0 0 18 18", fill: "none" },
                React.createElement("path", { d: "M3 9h12M9 3v12", stroke: COLORS.accent, strokeWidth: 2, strokeLinecap: "round" }),
                React.createElement("circle", { cx: 9, cy: 9, r: 8, stroke: COLORS.accent, strokeWidth: 1.5 })
              )
            ),
            React.createElement("div", null,
              React.createElement("div", { style: { fontSize: 15, fontWeight: 700, color: COLORS.textDark } }, "Build your estimate"),
              React.createElement("div", { style: { fontSize: 12, color: COLORS.textDim } }, "Turn on the AI steps your process uses, adjust volumes per role")
            )
          ),

          // Roles per month row
          React.createElement("div", {
            style: { display: "flex", alignItems: "center", gap: 14, padding: "14px 16px", borderRadius: 12, background: "#1F1140", marginBottom: 12 }
          },
            React.createElement("div", { style: { width: 36, height: 36, borderRadius: 10, background: "rgba(255,255,255,0.1)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17, flexShrink: 0 } }, "📋"),
            React.createElement("div", { style: { flex: 1 } },
              React.createElement("div", { style: { fontSize: 13, fontWeight: 700, color: "#fff" } }, "Roles filled per month"),
              React.createElement("div", { style: { fontSize: 11, color: "rgba(255,255,255,0.5)", marginTop: 1 } }, "How many positions do you hire for each month?")
            ),
            React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6 } },
              React.createElement("button", {
                onClick: () => setRoles(Math.max(1, roles - 1)),
                style: { width: 30, height: 30, borderRadius: "8px 0 0 8px", border: "1px solid rgba(255,255,255,0.2)", borderRight: 0, background: "rgba(255,255,255,0.08)", cursor: "pointer", fontFamily: "inherit", fontSize: 18, color: "#fff", fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center" }
              }, "−"),
              React.createElement("div", {
                style: { minWidth: 44, height: 30, border: "1px solid rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, fontWeight: 700, color: "#fff", background: "rgba(255,255,255,0.05)" }
              }, roles),
              React.createElement("button", {
                onClick: () => setRoles(Math.min(100, roles + 1)),
                style: { width: 30, height: 30, borderRadius: "0 8px 8px 0", border: "1px solid rgba(255,255,255,0.2)", borderLeft: 0, background: "rgba(255,255,255,0.08)", cursor: "pointer", fontFamily: "inherit", fontSize: 18, color: "#fff", fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center" }
              }, "+")
            ),
            React.createElement("div", { style: { minWidth: 80, textAlign: "right" } },
              React.createElement("span", { style: { fontSize: 17, fontWeight: 700, color: "#94E022", letterSpacing: -0.5 } }, roles),
              React.createElement("span", { style: { fontSize: 11, color: "rgba(255,255,255,0.45)", marginLeft: 3 } }, "roles/mo")
            )
          ),

          // Connector dot
          React.createElement("div", { style: { display: "flex", alignItems: "center", paddingLeft: 34, gap: 6, marginBottom: 6 } },
            React.createElement("div", { style: { width: 1, height: 12, background: "#DDD6FE" } }),
            React.createElement("span", { style: { fontSize: 10, color: COLORS.textDim, letterSpacing: 1, fontWeight: 600 } }, "EACH ROLE GOES THROUGH")
          ),

          // Stage rows
          React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 8 } },
            stageRow("📞", "AI Screening", "Text messages or phone calls — each counts as 1 credit", useScreens, setUseScreens, "tog-s", aiScreens, setAiScreens, 1, 50, roles * aiScreens),
            stageRow("🎥", "Video Interview", "Async or live AI-led video screen — 1 credit per candidate", useVideo, setUseVideo, "tog-v", videoInt, setVideoInt, 1, 30, roles * videoInt),
            stageRow("📝", "AI Notetaker", "Structured interview with a human — AI records and scores", useNote, setUseNote, "tog-n", notetaker, setNotetaker, 1, 15, roles * notetaker)
          )
        ),

        // Right: live estimate panel
        React.createElement("div", {
          style: { padding: "32px 28px", background: isOverAll ? "#FFF1F2" : creditsEst === 0 ? "#FAFAFA" : "#F9F5FF", display: "flex", flexDirection: "column", justifyContent: "space-between" }
        },
          React.createElement("div", null,
            React.createElement("div", { style: { fontSize: 11, fontWeight: 700, letterSpacing: 1.5, color: isOverAll ? "#E11D48" : COLORS.accent, marginBottom: 16 } },
              isOverAll ? "HIGH VOLUME" : "YOUR ESTIMATE"
            ),

            // Big credits number
            React.createElement("div", { style: { marginBottom: 20 } },
              React.createElement("div", {
                style: { fontSize: creditsEst >= 1000 ? 52 : 64, fontWeight: 700, letterSpacing: -2, color: COLORS.textDark, lineHeight: 1 }
              }, creditsEst === 0 ? "—" : creditsEst),
              React.createElement("div", { style: { fontSize: 13, color: COLORS.textDim, marginTop: 6 } },
                creditsEst === 0 ? "Enable at least one stage" : "credits / month"
              )
            ),

            // Breakdown
            creditsEst > 0 && React.createElement("div", {
              style: { background: "rgba(124,77,255,0.06)", borderRadius: 10, padding: "12px 14px", marginBottom: 20 }
            },
              React.createElement("div", { style: { fontSize: 11, fontWeight: 600, color: COLORS.textDim, letterSpacing: 0.5, marginBottom: 8 } }, "BREAKDOWN"),
              useScreens && React.createElement("div", { style: { display: "flex", justifyContent: "space-between", fontSize: 12, color: COLORS.textDark, marginBottom: 4 } },
                React.createElement("span", null, roles, " roles × ", aiScreens, " screens"),
                React.createElement("span", { style: { fontWeight: 700 } }, roles * aiScreens, " cr")
              ),
              useVideo && React.createElement("div", { style: { display: "flex", justifyContent: "space-between", fontSize: 12, color: COLORS.textDark, marginBottom: 4 } },
                React.createElement("span", null, roles, " roles × ", videoInt, " videos"),
                React.createElement("span", { style: { fontWeight: 700 } }, roles * videoInt, " cr")
              ),
              useNote && React.createElement("div", { style: { display: "flex", justifyContent: "space-between", fontSize: 12, color: COLORS.textDark, marginBottom: 4 } },
                React.createElement("span", null, roles, " roles × ", notetaker, " notes"),
                React.createElement("span", { style: { fontWeight: 700 } }, roles * notetaker, " cr")
              ),
              React.createElement("div", { style: { borderTop: "1px solid rgba(124,77,255,0.12)", marginTop: 6, paddingTop: 6, display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 700, color: COLORS.textDark } },
                React.createElement("span", null, "Total"),
                React.createElement("span", { style: { color: COLORS.accent } }, creditsEst, " cr/mo")
              )
            ),

            // Recommended plan
            creditsEst > 0 && !isOverAll && React.createElement("div", {
              style: { background: COLORS.accent, borderRadius: 12, padding: "14px 16px" }
            },
              React.createElement("div", { style: { fontSize: 10, fontWeight: 700, letterSpacing: 1.5, color: "rgba(255,255,255,0.65)", marginBottom: 4 } }, "RECOMMENDED"),
              React.createElement("div", { style: { fontSize: 20, fontWeight: 700, color: "#fff", letterSpacing: -0.5 } }, recommended.id),
              React.createElement("div", { style: { fontSize: 12, color: "rgba(255,255,255,0.7)", marginTop: 2 } },
                recommended.credits, " credits/mo · ", recommended.credits - creditsEst, " headroom"
              )
            ),

            isOverAll && React.createElement("div", {
              style: { background: "#E11D48", borderRadius: 12, padding: "14px 16px" }
            },
              React.createElement("div", { style: { fontSize: 10, fontWeight: 700, letterSpacing: 1.5, color: "rgba(255,255,255,0.65)", marginBottom: 4 } }, "VOLUME TOO HIGH"),
              React.createElement("div", { style: { fontSize: 16, fontWeight: 700, color: "#fff" } }, "Custom plan needed"),
              React.createElement("div", { style: { fontSize: 12, color: "rgba(255,255,255,0.7)", marginTop: 2 } }, "Let's build something for you")
            )
          ),

          React.createElement("button", {
            onClick: () => onStarted(null),
            style: { marginTop: 24, width: "100%", background: isOverAll ? "#E11D48" : COLORS.accent, color: "#fff", border: "none", borderRadius: 10, padding: "13px 18px", fontSize: 13, fontWeight: 700, cursor: "pointer", fontFamily: "inherit" }
          }, isOverAll ? "Speak to sales →" : "Get started →")
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
          const isBest     = !isOverAll && creditsEst > 0 && p.id === recommended.id;
          const monthlyEff = annual ? p.monthly * 0.8 : p.monthly;
          const perCredit  = monthlyEff / p.credits;

          return React.createElement("div", {
            key: p.id,
            style: {
              background: isBest ? "#FDFAFF" : "#fff",
              border: (isBest ? "2px" : "1px") + " solid " + (isBest ? COLORS.accent : COLORS.borderLight),
              borderRadius: 16, padding: 24, position: "relative",
              display: "flex", flexDirection: "column",
              boxShadow: isBest ? "0 0 0 4px rgba(124,77,255,0.08)" : "none",
              transition: "box-shadow 0.25s, border-color 0.25s"
            }
          },
            isBest && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: COLORS.accent, color: "#fff", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, creditsEst > 0 ? "BEST FIT FOR YOU" : "MOST POPULAR"),

            !isBest && p.popular && React.createElement("div", {
              style: { position: "absolute", top: -12, left: "50%", transform: "translateX(-50%)", background: creditsEst > 0 ? "#E4E4E7" : COLORS.accent, color: creditsEst > 0 ? "#6A6A74" : "#fff", fontSize: 11, fontWeight: 700, padding: "4px 12px", borderRadius: 12, letterSpacing: 0.4, whiteSpace: "nowrap" }
            }, "MOST POPULAR"),

            React.createElement("div", { style: { fontSize: 15, fontWeight: 700, color: COLORS.textDark, letterSpacing: 0.2 } }, p.id),

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

            React.createElement("div", { style: { borderTop: "1px solid " + COLORS.borderLight, margin: "18px 0 14px" } }),

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

            React.createElement("div", {
              title: "Extra interactions at " + p.overage + "/credit — no hard cap.",
              style: { display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11, color: COLORS.textDim, cursor: "help", borderBottom: "1px dashed " + COLORS.borderLight, paddingBottom: 1, alignSelf: "flex-start", marginBottom: 18 }
            },
              "Overage ", React.createElement("span", { style: { color: COLORS.textDark, fontWeight: 600 } }, p.overage), "/credit"
            ),

            React.createElement("button", {
              onClick: () => onStarted(null),
              style: { marginTop: "auto", width: "100%", background: isBest ? COLORS.accent : "transparent", color: isBest ? "#fff" : COLORS.accent, border: "1px solid " + COLORS.accent, borderRadius: 10, padding: "12px 18px", fontSize: 13, fontWeight: 700, cursor: "pointer", fontFamily: "inherit" }
            }, "Get started")
          );
        })
      ),

      // ── Overage risk strip (low prominence, below plan cards)
      (() => {
        if (creditsEst === 0 || isOverAll) return null;
        const recIdx   = plans.findIndex(p => p.id === recommended.id);
        if (recIdx === 0) return null; // already on cheapest plan — no near-miss
        const nearMiss = plans[recIdx - 1];
        const overRate = parseFloat(nearMiss.overage.replace("$",""));
        const overCr   = creditsEst - nearMiss.credits;
        const overCost = Math.round(overCr * overRate);
        const nmTotal  = Math.round((annual ? nearMiss.monthly * 0.8 : nearMiss.monthly) + overCost);
        const recPrice = Math.round(annual ? recommended.monthly * 0.8 : recommended.monthly);
        const saving   = nmTotal - recPrice;

        return React.createElement("div", {
          style: { margin: "20px 0 0", padding: "14px 20px", borderRadius: 12, background: "#FFFBEB", border: "1px solid #FDE68A", display: "flex", alignItems: "flex-start", gap: 10 }
        },
          // Info icon
          React.createElement("svg", { width: 15, height: 15, viewBox: "0 0 16 16", fill: "none", style: { flexShrink: 0, marginTop: 1 } },
            React.createElement("circle", { cx: 8, cy: 8, r: 7, stroke: "#D97706", strokeWidth: 1.4 }),
            React.createElement("path", { d: "M8 7v4", stroke: "#D97706", strokeWidth: 1.5, strokeLinecap: "round" }),
            React.createElement("circle", { cx: 8, cy: 5.2, r: 0.8, fill: "#D97706" })
          ),
          React.createElement("p", { style: { margin: 0, fontSize: 12, color: "#92400E", lineHeight: 1.6 } },
            React.createElement("strong", { style: { fontWeight: 700 } }, nearMiss.id, " overage check: "),
            "at ", creditsEst, " credits/mo you'd use ", overCr, " credits above the ", nearMiss.credits, "-credit cap — that's ~$", overCost, "/mo extra, pushing your total to ~$", nmTotal, "/mo. ",
            React.createElement("strong", { style: { fontWeight: 700 } }, recommended.id),
            " at $", recPrice, "/mo covers you fully",
            saving > 0 ? React.createElement("span", null, " and saves ~$", saving, "/mo over sticking with ", nearMiss.id, " on overages") : null,
            "."
          )
        );
      })(),

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

out = 'variant-2-calculator.html'
with open(out, 'w') as f:
    f.write(new_html)
print(f"Written: {out}  ({len(new_html):,} bytes)")
