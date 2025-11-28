// Grade Horária - Sistema de Drag & Drop com LocalStorage
// Paleta de cores para disciplinas
const palette = ["#2563eb","#16a34a","#db2777","#f59e0b","#7c3aed","#059669","#dc2626","#0ea5e9"];

// Carregar disciplinas do banco de dados (passadas pelo template)
const baseCourses = (window.coursesFromDB || []).map((c, i) => ({
  ...c,
  color: palette[i % palette.length]
}));

// Configuração da grade
const HOURS = Array.from({length: 10}, (_, i) => 7 + i); // 7h até 16h
const DAYS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
const tbody = document.querySelector("#grid tbody");

// Estado da aplicação
const state = {
  busy: {},      // Mapa de slots ocupados
  instances: {}  // Instâncias de disciplinas na grade
};

// Persistência no LocalStorage
const save = () => localStorage.setItem("gradeState2h", JSON.stringify(state));
const load = () => {
  try {
    const raw = localStorage.getItem("gradeState2h");
    if (!raw) return;
    const s = JSON.parse(raw);
    if (s && s.instances && s.busy) {
      Object.assign(state, s);
    }
  } catch (e) {
    console.warn("Falha ao carregar:", e);
  }
};

// Construir a grade de horários
function buildGrid() {
  tbody.innerHTML = "";
  HOURS.forEach(hour => {
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.className = "p-3 border border-blue-900 text-left font-semibold whitespace-nowrap";
    th.textContent = `${hour}h - ${hour + 1}h`;
    tr.appendChild(th);
    
    DAYS.forEach((day, dayIndex) => {
      const td = document.createElement("td");
      td.className = "align-top p-2 border border-blue-900 h-16 min-w-32";
      td.dataset.day = dayIndex;
      td.dataset.hour = hour;
      td.addEventListener("dragover", onDragOver);
      td.addEventListener("dragleave", onDragLeave);
      td.addEventListener("drop", onDrop);
      tr.appendChild(td);
    });
    
    tbody.appendChild(tr);
  });
}

// Construir sidebar de disciplinas
function buildSidebar(courses = baseCourses) {
  const list = document.getElementById("courseList");
  list.innerHTML = "";
  
  courses.forEach(course => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="class-chip flex items-center justify-between bg-white border rounded-lg p-2 shadow-sm" 
           draggable="true" 
           data-code="${course.code}" 
           data-name="${course.name}" 
           data-color="${course.color}">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full" style="background:${course.color}"></span>
          <div>
            <div class="font-semibold text-sm">${course.code}</div>
            <div class="text-xs text-slate-600">${course.name}</div>
          </div>
        </div>
        <span class="material-icons text-slate-500">drag_indicator</span>
      </div>
    `;
    
    const chip = li.firstElementChild;
    chip.addEventListener("dragstart", onDragStartFromSidebar);
    list.appendChild(li);
  });
}

// Drag and Drop
let dragPayload = null;

function onDragStartFromSidebar(e) {
  const chip = e.currentTarget;
  dragPayload = {
    code: chip.dataset.code,
    name: chip.dataset.name,
    color: chip.dataset.color,
    duration: 2
  };
  e.dataTransfer.setData("text/plain", JSON.stringify(dragPayload));
}

function onDragOver(e) {
  e.preventDefault();
  const cell = e.currentTarget;
  const canDrop = canPlace(cell, 2);
  cell.classList.toggle("drop-ok", canDrop);
  cell.classList.toggle("drop-bad", !canDrop);
}

function onDragLeave(e) {
  const cell = e.currentTarget;
  cell.classList.remove("drop-ok", "drop-bad");
}

function onDrop(e) {
  e.preventDefault();
  const cell = e.currentTarget;
  cell.classList.remove("drop-ok", "drop-bad");
  
  const data = dragPayload || JSON.parse(e.dataTransfer.getData("text/plain") || "{}");
  if (!data) return;
  
  const day = parseInt(cell.dataset.day, 10);
  const hour = parseInt(cell.dataset.hour, 10);
  placeInstance(data, day, hour, 2);
}

// Verificar se pode colocar disciplina
function canPlace(cell, duration) {
  const day = parseInt(cell.dataset.day, 10);
  const hour = parseInt(cell.dataset.hour, 10);
  
  for (let i = 0; i < duration; i++) {
    const slot = `${day}-${hour + i}`;
    if (!HOURS.includes(hour + i) || state.busy[slot]) {
      return false;
    }
  }
  return true;
}

// Colocar disciplina na grade
function placeInstance(course, day, startHour, duration = 2) {
  // Validar disponibilidade
  for (let i = 0; i < duration; i++) {
    const slot = `${day}-${startHour + i}`;
    if (!HOURS.includes(startHour + i)) {
      toast("Duração excede a grade.");
      return;
    }
    if (state.busy[slot]) {
      toast("Conflito: horário já ocupado.");
      return;
    }
  }
  
  // Criar instância
  const id = `i${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const instance = {
    id,
    code: course.code,
    name: course.name,
    color: course.color,
    day,
    startHour,
    duration
  };
  
  state.instances[id] = instance;
  
  // Marcar slots como ocupados
  for (let i = 0; i < duration; i++) {
    const slot = `${day}-${instance.startHour + i}`;
    state.busy[slot] = i === 0 ? id : `${id}:cont`;
  }
  
  renderInstance(instance);
  save();
}

// Renderizar disciplina na grade
function renderInstance(instance) {
  for (let i = 0; i < instance.duration; i++) {
    const cell = tbody.querySelector(`td[data-day="${instance.day}"][data-hour="${instance.startHour + i}"]`);
    if (!cell) continue;
    
    cell.classList.add("slot-occupied");
    const block = document.createElement("div");
    block.className = "select-none text-white rounded-lg px-2 py-1 shadow flex items-center justify-between";
    block.style.background = instance.color;
    block.dataset.id = instance.id;
    
    // Todos os blocos mostram as informações completas
    block.innerHTML = `
      <div class="text-left">
        <div class="font-semibold leading-tight">${instance.code}</div>
        <div class="text-[11px] opacity-90">${instance.name}</div>
        <div class="text-[11px] opacity-90">${DAYS[instance.day]} · ${instance.startHour}h–${instance.startHour + instance.duration}h</div>
      </div>
      <button class="bg-white/20 px-1.5 py-0.5 rounded" title="Remover" data-act="del">
        <span class="material-icons text-sm">close</span>
      </button>
    `;
    block.querySelector("[data-act=\"del\"]").addEventListener("click", () => removeInstance(instance.id));
    
    cell.appendChild(block);
  }
}

// Remover disciplina da grade
function removeInstance(id) {
  const instance = state.instances[id];
  if (!instance) return;
  
  // Limpar slots ocupados
  for (let i = 0; i < instance.duration; i++) {
    const slot = `${instance.day}-${instance.startHour + i}`;
    delete state.busy[slot];
    
    const cell = tbody.querySelector(`td[data-day="${instance.day}"][data-hour="${instance.startHour + i}"]`);
    if (cell) {
      cell.classList.remove("slot-occupied");
      cell.innerHTML = "";
    }
  }
  
  delete state.instances[id];
  save();
}

// Botões de ação
document.getElementById("btnExport").addEventListener("click", () => {
  const data = Object.values(state.instances).map(inst => ({
    código: inst.code,
    disciplina: inst.name,
    dia: DAYS[inst.day],
    início: `${inst.startHour}:00`,
    término: `${inst.startHour + inst.duration}:00`
  }));
  
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "grade_2h.json";
  a.click();
  URL.revokeObjectURL(url);
});

document.getElementById("btnClear").addEventListener("click", () => {
  if (confirm("Deseja limpar toda a grade?")) {
    Object.keys(state.instances).forEach(removeInstance);
    save();
  }
});

// Busca de disciplinas
document.getElementById("search").addEventListener("input", e => {
  const query = e.target.value.trim().toLowerCase();
  const filtered = baseCourses.filter(c => 
    `${c.code} ${c.name}`.toLowerCase().includes(query)
  );
  buildSidebar(filtered);
});

// Toast de notificações
let toastTimer;
function toast(message) {
  clearTimeout(toastTimer);
  let el = document.getElementById("toast");
  
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    el.className = "fixed bottom-4 left-1/2 -translate-x-1/2 bg-black text-white px-3 py-2 rounded-lg text-sm shadow-lg";
    document.body.appendChild(el);
  }
  
  el.textContent = message;
  el.style.opacity = "1";
  toastTimer = setTimeout(() => {
    el.style.opacity = "0";
  }, 1800);
}

// Renderizar todas as instâncias salvas
function renderAll() {
  tbody.querySelectorAll("td").forEach(cell => {
    cell.classList.remove("slot-occupied");
    cell.innerHTML = "";
  });
  Object.values(state.instances).forEach(renderInstance);
}

// Inicialização
buildGrid();
buildSidebar();
load();
renderAll();
