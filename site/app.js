// Renders site/data.json. Repo text comes from GitHub, so everything goes in via textContent.
(() => {
  const state = { data: null, view: "trending", sort: "rank", tag: null };
  const $ = (id) => document.getElementById(id);
  const num = new Intl.NumberFormat("en-US");
  const compact = new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 });
  const VIEWS = ["trending", "lens", "baseline"];
  const BADGES = { production: "Production-ready", pilot: "Pilot in lab", experimental: "Experimental" };
  const RANK_FIELD = { trending: "trend_rank", lens: "lens_rank" };

  function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") node.className = v;
      else node.setAttribute(k, v === true ? "" : v);
    }
    for (const child of children.flat()) {
      if (child == null || child === false) continue;
      node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    }
    return node;
  }

  const LANGS = { powershell: "PowerShell", shell: "Shell", hcl: "HCL", python: "Python", go: "Go", swift: "Swift" };

  function pct(w) { return `${Math.round(w * 100)}%`; }
  function languages() {
    return state.data.methodology.trending_languages.filter((l) => l !== "all").map((l) => LANGS[l] || l).join(", ");
  }

  function intro(view) {
    return {
      trending: `IT-relevant repos ranked by momentum: stars gained, days on GitHub Trending (the global page plus ${languages()}), and total stars.`,
      lens: "Repos that pass the validation gate, ranked by how much they would actually help a sysadmin (fit 0–3) and then by deploy-safety. Each one comes with a \"why\" and a safe first step.",
      baseline: "What an AI-ready IT stack looks like, domain by domain: scriptable APIs first, then read-only agent access, then scoped write access with approvals, then your team's know-how written down as skills.",
    }[view];
  }

  // -- cards ------------------------------------------------------------------

  function trustBadge(r) {
    if (!r || !r.trust_badge) return null;
    return el("span", { class: `badge ${r.trust_badge}`, title: `Trust ${r.trust_score}/100 · ${r.trust_reasons.join(" · ")}` },
      BADGES[r.trust_badge]);
  }

  function readOnlyBadge(r) {
    return r && r.readonly_mode === true && r.tags.includes("agent")
      ? el("span", { class: "badge ro", title: "Documents a read-only mode or read-only scopes" }, "Read-only mode")
      : null;
  }

  function repoLink(r) {
    const [owner, name] = r.full_name.split("/");
    return el("a", { class: "repo", href: r.url, target: "_blank", rel: "noopener" },
      el("span", { class: "owner" }, `${owner} / `), name);
  }

  function card(key) {
    const r = state.data.repos[key];
    const labels = Object.fromEntries(state.data.tags.map((t) => [t.id, t.label]));
    const rank = r[RANK_FIELD[state.view]];
    const history = state.data.methodology.history_days;
    const gained = `${r.stars_gained_estimated ? "≈" : "+"}${num.format(r.stars_gained_30d)}`;
    return el("article", { class: "card" },
      el("div", { class: "card-head" },
        el("span", { class: "rank", title: state.view === "lens" ? "IT Ops lens rank" : "Composite trending rank" }, `#${rank}`),
        repoLink(r)),
      r.description && el("p", { class: "desc" }, r.description),
      r.why && el("p", { class: "why" }, el("strong", {}, "Why for sysadmins"), r.why),
      state.view === "lens" && r.first_step && el("p", { class: "step" }, el("b", {}, "First safe step: "), r.first_step),
      r.tags.length > 0 && el("div", { class: "tags" }, r.tags.map((t) => el("span", { class: "tag" }, labels[t] || t))),
      el("div", { class: "stats" },
        el("span", { title: "Total stars" }, "★ ", el("b", {}, compact.format(r.stars))),
        el("span", { title: r.stars_gained_estimated ? "Stars gained in 30 days (estimated from recent rate)" : "Stars gained in 30 days" },
          el("b", {}, gained), " in 30d"),
        history > 0 && el("span", { title: `Days on a daily trending page, out of ${history} days of history` },
          el("b", {}, r.times_trending_30d), r.times_trending_30d === 1 ? " trending day" : " trending days"),
        r.fit != null && el("span", { title: r.scored_by === "human" ? "Fit set by a human reviewer" : "Fit from Claude's first pass, human-reviewed" },
          "Fit ", el("b", {}, `${r.fit}/3`)),
        trustBadge(r),
        readOnlyBadge(r)));
  }

  function renderList() {
    const keys = state.data.views[state.view].filter((k) => !state.tag || state.data.repos[k].tags.includes(state.tag));
    const field = RANK_FIELD[state.view];
    const sorted = [...keys].sort((a, b) => {
      const ra = state.data.repos[a], rb = state.data.repos[b];
      return state.sort === "rank" ? ra[field] - rb[field] : (rb[state.sort] ?? 0) - (ra[state.sort] ?? 0);
    });
    const view = $("view");
    view.replaceChildren(sorted.length
      ? el("div", { class: "grid" }, sorted.map(card))
      : el("p", { class: "empty" }, state.data.views[state.view].length
        ? "No repos with that tag in this view."
        : "Nothing has passed the gate yet. The first weekly refresh fills this in."));
  }

  function renderFilters() {
    const present = new Set(state.data.views[state.view].flatMap((k) => state.data.repos[k].tags));
    const chip = (id, label) => {
      const b = el("button", { class: "chip", type: "button", "aria-pressed": String(state.tag === id) }, label);
      b.addEventListener("click", () => { state.tag = id; renderFilters(); renderList(); });
      return b;
    };
    $("filters").replaceChildren(chip(null, "All"),
      ...state.data.tags.filter((t) => present.has(t.id)).map((t) => chip(t.id, t.label)));
  }

  // -- baseline ---------------------------------------------------------------

  function entry(e) {
    const repoUrl = state.data.source_repo ? `https://github.com/${state.data.source_repo}/tree/main/` : null;
    if (e.idea) return el("div", { class: "entry idea" }, el("div", { class: "name" }, e.idea), e.note && el("p", {}, e.note));
    if (e.skill) {
      const name = e.skill.split("/").pop();
      return el("div", { class: "entry" },
        el("div", { class: "name" }, repoUrl ? el("a", { href: repoUrl + e.skill, target: "_blank", rel: "noopener" }, `Skill: ${name}`) : `Skill: ${name}`),
        e.note && el("p", {}, e.note));
    }
    const r = state.data.repos[e.key];
    return el("div", { class: "entry" },
      el("div", { class: "name" }, el("a", { href: r ? r.url : `https://github.com/${e.repo}`, target: "_blank", rel: "noopener" }, e.repo)),
      el("div", { class: "badges" },
        e.unverified ? el("span", { class: "badge unverified", title: "GitHub could not find this repo on the last refresh" }, "Unverified") : trustBadge(r),
        readOnlyBadge(r),
        r && el("span", { class: "tag" }, `★ ${compact.format(r.stars)}`)),
      e.note && el("p", {}, e.note));
  }

  function renderBaseline() {
    const b = state.data.baseline;
    const matrix = el("div", { class: "matrix", role: "table", "aria-label": "Readiness matrix" },
      el("div", { class: "mx-head", role: "columnheader" }, el("b", {}, "Domain")),
      b.levels.map((l) => el("div", { class: "mx-head", role: "columnheader" }, el("b", {}, `${l.id} · ${l.label}`), el("span", {}, l.description))));
    for (const d of b.domains) {
      matrix.append(el("div", { class: "mx-domain", role: "rowheader" }, d.label));
      b.levels.forEach((l, i) => {
        const items = d.cells[l.id] || [];
        matrix.append(el("div", { class: `mx-cell${i === b.levels.length - 1 ? " last" : ""}`, role: "cell" },
          el("span", { class: "mx-level" }, `${l.id} · ${l.label}`),
          items.length ? items.map(entry) : el("span", { class: "gap" }, "Nothing we'd trust here yet")));
      });
    }
    $("view").replaceChildren(
      el("h2", {}, "Foundations"),
      el("div", { class: "foundations" }, b.foundations.map((f) => el("div", { class: "foundation" }, entry(f)))),
      el("h2", {}, "Readiness matrix"),
      matrix,
      el("h2", {}, "Baseline checklist"),
      el("ol", { class: "checklist" }, b.checklist.map((c) => el("li", {}, el("b", {}, c.title), el("p", {}, c.detail)))));
  }

  // -- methodology ------------------------------------------------------------

  function renderMethod() {
    const m = state.data.methodology;
    const w = m.weights, g = m.gate, t = m.trust;
    const fit = Object.entries(m.fit_scale).sort((a, b) => b[0] - a[0]);
    $("method-body").replaceChildren(
      el("h3", {}, "Trending (default)"),
      el("p", {}, `IT-relevant candidates (they match at least one IT domain in the rubric) are normalized across the pool and scored: `,
        `${pct(w.stars_gained)} stars gained (${m.window_days}d) · ${pct(w.times_trending)} times trending (${m.window_days}d) · ${pct(w.total_stars)} total stars. `,
        `Stars gained and times trending are max-normalized${m.log_total_stars ? "; total stars are log-normalized so one giant repo doesn't flatten the rest" : ""}. `,
        `Times trending counts distinct days on any daily GitHub Trending page (global or ${languages()}). `,
        `History collected so far: ${m.history_days} of ${m.window_days} days.`),
      el("h3", {}, "IT Ops lens"),
      el("p", {}, `The pool is 7d and 30d trending, GitHub topic search across IT topics, nominations, and every repo in the baseline matrix. `,
        `It is gated to validated repos (≥${num.format(g.min_stars)} stars, or ≥${g.min_stars_gained_30d} stars gained in 30 days, or trended ≥${g.min_times_trending_30d}×), `,
        `and each one must also be unarchived, pushed in the last ${g.max_days_since_push} days${g.require_license ? ", and openly licensed" : ""}. `,
        `Each repo gets a 0–3 fit score: Claude scores it first, and a human approves or overrides that score in a pull request.`),
      el("ul", {}, fit.map(([k, v]) => el("li", {}, el("b", {}, `${k}: `), v))),
      el("p", {}, `The top ${m.show.lens} are ranked by fit, then trust, then momentum.`),
      el("h3", {}, "Trust badge"),
      el("p", {}, `Deploy-safety out of 100: maintenance ${t.points.maintenance}, releases ${t.points.releases}, contributors ${t.points.community}, `,
        `license ${t.points.license}, provenance ${t.points.provenance} (vendor, community or personal), OpenSSF Scorecard ${t.points.scorecard}. `,
        `Agent tools get +${t.readonly_bonus} for a documented read-only mode and −${t.readonly_penalty} when they need write access. `,
        `Production-ready ≥${t.badges.production} · Pilot in lab ≥${t.badges.pilot} · otherwise Experimental. Hover a badge to see the reasons behind it.`),
      el("p", {}, "Sorting re-orders cards; the # badge is the composite rank in Trending and the lens rank in IT Ops lens."));
  }

  // -- shell ------------------------------------------------------------------

  function select(view) {
    state.view = VIEWS.includes(view) ? view : "trending";
    state.tag = null;
    for (const b of document.querySelectorAll(".tabs button")) {
      b.setAttribute("aria-selected", String(b.dataset.view === state.view));
      b.tabIndex = b.dataset.view === state.view ? 0 : -1;
    }
    $("view").setAttribute("aria-labelledby", `tab-${state.view}`);
    $("intro").textContent = intro(state.view);
    $("controls").hidden = state.view === "baseline";
    if (state.view === "baseline") renderBaseline();
    else { renderFilters(); renderList(); }
  }

  function start(data) {
    state.data = data;
    const updated = new Date(data.generated_at).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
    $("meta").textContent = `Updated ${updated} · refreshed weekly, human-reviewed`;
    for (const b of document.querySelectorAll(".tabs button")) {
      b.addEventListener("click", () => { history.replaceState(null, "", `#${b.dataset.view}`); select(b.dataset.view); });
    }
    $("sort").addEventListener("change", (e) => { state.sort = e.target.value; renderList(); });
    window.addEventListener("hashchange", () => select(location.hash.slice(1)));
    renderMethod();
    select(location.hash.slice(1));
  }

  fetch("data.json", { cache: "no-cache" })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(start)
    .catch(() => {
      $("view").replaceChildren(el("p", { class: "empty" }, "No data yet. Run the Refresh workflow and merge its pull request."));
      $("method").hidden = true;
    });
})();
