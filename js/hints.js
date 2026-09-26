// Gemeinsame Logik für alle Hilfekarten-Sets.
//
// Wartezeit zwischen zwei Hinweisen (in Sekunden), pro Set:
//   <main class="hilfekarten" data-wartezeit="60">
// Optional abweichend für eine einzelne Aufgabe:
//   <section class="task" data-wartezeit="120">
(function () {
  const root = document.querySelector(".hilfekarten");
  if (!root) return;

  const setWait = parseInt(root.dataset.wartezeit, 10);
  const defaultWait = isNaN(setWait) ? 60 : setWait;
  const tasks = Array.from(root.querySelectorAll(".task"));
  if (!tasks.length) return;

  // Fortschritt pro Aufgabe merken (überlebt Neuladen der Seite)
  const storeKey = "hilfekarten:" + location.pathname;
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storeKey)) || {}; } catch (e) {}
  if (!saved.tasks) saved.tasks = {};
  function save() {
    try { localStorage.setItem(storeKey, JSON.stringify(saved)); } catch (e) {}
  }

  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  function fmt(ms) {
    const s = Math.ceil(ms / 1000);
    return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
  }

  // Jede .task in eine Karte umbauen
  const cards = tasks.map(function (task, idx) {
    const id = task.id || "task" + (idx + 1);
    const label = task.dataset.label || "Aufgabe " + (idx + 1);
    const h2 = task.querySelector(":scope > h2");
    const title = h2 ? h2.innerHTML : "";
    const wait = parseInt(task.dataset.wartezeit, 10);
    const waitMs = (isNaN(wait) ? defaultWait : wait) * 1000;

    const hintEls = Array.from(task.querySelectorAll(":scope > .hint"));
    hintEls.forEach(function (h) { h.remove(); });
    task.querySelectorAll(":scope > button").forEach(function (b) { b.remove(); });
    if (h2) h2.remove();
    const rest = Array.from(task.childNodes);
    task.textContent = "";
    task.classList.add("card");
    task.hidden = true;

    const head = el("div", "card-head");
    const headText = el("div");
    headText.appendChild(el("p", "card-label", label));
    if (title) headText.appendChild(el("h2", "", title));
    const progress = el("div", "progress");
    progress.setAttribute("aria-hidden", "true");
    hintEls.forEach(function () { progress.appendChild(el("span")); });
    head.appendChild(headText);
    head.appendChild(progress);
    task.appendChild(head);

    const hasContent = rest.some(function (n) {
      return n.nodeType === 1 || (n.nodeType === 3 && n.textContent.trim());
    });
    if (hasContent) {
      const aufgabe = el("div", "aufgabe");
      rest.forEach(function (n) { aufgabe.appendChild(n); });
      task.appendChild(aufgabe);
    }

    const list = el("ol", "hints");
    list.setAttribute("aria-live", "polite");
    const empty = el("li", "empty", "Noch kein Hinweis aufgedeckt. Probiere es zuerst selbst.");
    list.appendChild(empty);
    const items = hintEls.map(function (h, i) {
      // Alte Vorsilbe "Hinweis 1:" entfernen, die Nummer setzt das Skript selbst
      const first = h.firstChild;
      if (first && first.nodeType === 3) {
        first.textContent = first.textContent.replace(/^\s*Hinweis\s*\d+\s*:\s*/, "");
      }
      const li = el("li", "hint");
      li.hidden = true;
      li.appendChild(el("span", "hint-no", String(i + 1)));
      const body = el("div", "hint-body");
      body.appendChild(el("span", "hint-label", "Hinweis " + (i + 1)));
      const text = el("div", "hint-text");
      while (h.firstChild) text.appendChild(h.firstChild);
      body.appendChild(text);
      li.appendChild(body);
      list.appendChild(li);
      return li;
    });
    task.appendChild(list);

    const foot = el("div", "card-foot");
    const btn = el("button", "next");
    btn.type = "button";
    const fill = el("span", "fill");
    const lbl = el("span", "lbl");
    btn.appendChild(fill);
    btn.appendChild(lbl);
    const status = el("p", "status");
    foot.appendChild(btn);
    foot.appendChild(status);
    task.appendChild(foot);

    const card = {
      id: id, label: label, title: h2 ? h2.textContent.trim() : "",
      node: task, items: items, empty: empty, progress: progress,
      btn: btn, fill: fill, lbl: lbl, status: status, waitMs: waitMs
    };
    if (!saved.tasks[id]) saved.tasks[id] = { shown: 0, last: 0 };
    btn.addEventListener("click", function () { reveal(card); });
    return card;
  });

  // Auswahl der Aufgaben (nur bei mehr als einer Aufgabe)
  const picker = el("div", "picker");
  picker.setAttribute("role", "group");
  picker.setAttribute("aria-label", "Aufgabe wählen");
  cards.forEach(function (card) {
    const b = el("button", "pick");
    b.type = "button";
    b.id = "pick-" + card.id;
    b.appendChild(el("span", "pick-num", card.label));
    if (card.title) {
      const t = el("span", "pick-title");
      t.textContent = card.title;
      b.appendChild(t);
    }
    b.addEventListener("click", function () { select(card.id); });
    card.pick = b;
    picker.appendChild(b);
  });
  if (cards.length > 1) tasks[0].before(picker);

  function st(card) { return saved.tasks[card.id]; }

  function remaining(card) {
    const s = st(card);
    if (s.shown === 0) return 0;
    return Math.max(0, card.waitMs - (Date.now() - s.last));
  }

  function render(card) {
    const s = st(card);
    card.empty.hidden = s.shown > 0;
    card.items.forEach(function (li, i) { li.hidden = i >= s.shown; });
    Array.from(card.progress.children).forEach(function (sp, i) {
      sp.classList.toggle("on", i < s.shown);
    });
    tick();
  }

  function reveal(card) {
    const s = st(card);
    if (s.shown >= card.items.length || remaining(card) > 0) return;
    const li = card.items[s.shown];
    li.classList.add("neu");
    s.shown += 1;
    s.last = Date.now();
    save();
    render(card);
  }

  let current = null;
  function select(id) {
    current = cards.find(function (c) { return c.id === id; }) || cards[0];
    cards.forEach(function (c) {
      c.node.hidden = c !== current;
      c.pick.setAttribute("aria-pressed", c === current ? "true" : "false");
    });
    saved.current = current.id;
    save();
    render(current);
  }

  function tick() {
    if (!current) return;
    const card = current;
    const s = st(card);
    const total = card.items.length;
    card.btn.classList.remove("waiting", "finished");

    if (s.shown >= total) {
      card.btn.disabled = true;
      card.btn.classList.add("finished");
      card.fill.style.transform = "scaleX(0)";
      card.lbl.textContent = total ? "Alle Hinweise aufgedeckt" : "Keine Hinweise";
      card.status.textContent = total ? "Mehr Hilfe gibt es hier nicht. Frage bei Bedarf deine Lehrkraft." : "";
      return;
    }

    const left = remaining(card);
    if (left > 0) {
      card.btn.disabled = true;
      card.btn.classList.add("waiting");
      card.fill.style.transform = "scaleX(" + (1 - left / card.waitMs) + ")";
      card.lbl.textContent = "Hinweis " + (s.shown + 1) + " in " + fmt(left);
      card.status.textContent = "Denkpause: Arbeite erst mit Hinweis " + s.shown + " weiter.";
    } else {
      card.btn.disabled = false;
      card.fill.style.transform = "scaleX(0)";
      card.lbl.textContent = "Hinweis " + (s.shown + 1) + " aufdecken";
      card.status.textContent = s.shown === 0
        ? total + (total === 1 ? " Hinweis" : " Hinweise") + ", die nach und nach mehr verraten."
        : "Kommst du nicht weiter? Dann decke den nächsten Hinweis auf.";
    }
  }

  select(saved.current);
  setInterval(tick, 250);
})();
