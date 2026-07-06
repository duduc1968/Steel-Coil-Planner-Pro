
const form = document.getElementById('form');
const btn = document.getElementById('btn');
const importBtn = document.getElementById('importBtn');
const cargoPreviewBox = document.getElementById('cargoPreviewBox');
const summaryBox = document.getElementById('summaryBox');
const weightsBox = document.getElementById('weightsBox');
const svg = document.getElementById('planSvg');
const sectionSvg = document.getElementById('sectionSvg');
const threeDSvg = document.getElementById('threeDSvg');
const threeDNote = document.getElementById('threeDNote');
const planTitle = document.getElementById('planTitle');
const viewTabs = document.querySelectorAll('.view-tab');
let currentView = 'top';
let lastPlanData = null;
const emptyPlan = document.getElementById('emptyPlan');
const legend = document.getElementById('legend');
const coilDetails = document.getElementById('coilDetails');
const uploadState = document.getElementById('uploadState');
const stowagePattern = document.getElementById('stowagePattern');
const activePatternTool = document.getElementById('activePatternTool');
const customPatternBox = document.getElementById('customPatternBox');
const customPattern = document.getElementById('customPattern');
const builderBox = document.getElementById('builderBox');
const builderPort = document.getElementById('builderPort');
const builderStbd = document.getElementById('builderStbd');
const builderWedge = document.getElementById('builderWedge');
const builderUpper = document.getElementById('builderUpper');
const builderPattern = document.getElementById('builderPattern');
const builderPreview = document.getElementById('builderPreview');
const shipLibraryTool = document.getElementById('shipLibraryTool');
const shipModal = document.getElementById('shipModal');
const closeShipModal = document.getElementById('closeShipModal');
const shipListBox = document.getElementById('shipListBox');
const shipLibraryStatus = document.getElementById('shipLibraryStatus');

let savedShips = [];
let selectedShipFile = null;
let currentShipConfig = {ship_name:'Default coaster', holds:[]};
let selectedHoldIndex = 0;
const libHoldSelector = document.getElementById('libHoldSelector');
let applyingVoyageSync = false;
let lastCargoPreview = null;

// v5.2: keep the Fleet Library in the browser as well as on the server.
// This prevents saved ship/hold data from being lost or reloaded with defaults after deploy/cache refresh.
const FLEET_KEY = 'scp_fleet_library_v52';
function clone(obj){ return JSON.parse(JSON.stringify(obj || {})); }
function localFleet(){
  try { return JSON.parse(localStorage.getItem(FLEET_KEY) || '[]'); }
  catch(e){ return []; }
}
function saveLocalFleet(list){
  localStorage.setItem(FLEET_KEY, JSON.stringify(list || []));
}
function shipKey(s){ return (s && (s._file || (s.ship_name || '').toLowerCase().trim())) || ''; }
function upsertLocalShip(ship){
  const s = clone(ship);
  if(!s._file) s._file = (s.ship_name || 'ship').replace(/[^a-zA-Z0-9_-]+/g,'_') + '.json';
  const list = localFleet();
  const key = shipKey(s);
  const idx = list.findIndex(x => shipKey(x) === key || (x.ship_name || '') === (s.ship_name || ''));
  if(idx >= 0) list[idx] = s; else list.unshift(s);
  saveLocalFleet(list);
  return s;
}
function mergeFleet(apiShips, localShips){
  const out = [];
  const seen = new Set();
  [...(localShips || []), ...(apiShips || [])].forEach(s => {
    const k = shipKey(s);
    if(!k || seen.has(k)) return;
    seen.add(k);
    out.push(s);
  });
  return out;
}

function fleetList(){
  return (savedShips && savedShips.length ? savedShips : localFleet()) || [];
}
function sameShipName(a,b){ return String(a||'').trim().toLowerCase() === String(b||'').trim().toLowerCase(); }
function findShipByName(name){ return fleetList().find(s => sameShipName(s.ship_name, name)); }
function ensureMainShipDropdown(selectedName){
  const sel = document.getElementById('shipName');
  const names = [];
  function addName(n){ n = String(n||'').trim(); if(n && !names.some(x=>sameShipName(x,n))) names.push(n); }
  addName(selectedName || sel.value);
  ['Default coaster','MV Drogdenbank','MV Varnebank','MV Vikingbank'].forEach(addName);
  fleetList().forEach(s => addName(s.ship_name));
  sel.innerHTML = names.map(n => `<option value="${n.replace(/"/g,'&quot;')}">${n}</option>`).join('');
  if(selectedName && names.some(n=>sameShipName(n, selectedName))) sel.value = names.find(n=>sameShipName(n, selectedName));
}
function renderVoyageHoldDropdown(ship, holdIndex=0){
  const holdSel = document.getElementById('holdName');
  const holds = (ship && ship.holds && ship.holds.length) ? ship.holds : [{hold_name:'Hold 1'}];
  holdSel.innerHTML = holds.map((h,i)=>`<option value="${String(h.hold_name || ('Hold '+(i+1))).replace(/"/g,'&quot;')}">${h.hold_name || ('Hold '+(i+1))}</option>`).join('');
  const idx = Math.max(0, Math.min(Number(holdIndex)||0, holds.length-1));
  holdSel.selectedIndex = idx;
}
function syncVoyageFromSelectedShipHold({closeModal=false, regenerate=false}={}){
  if(applyingVoyageSync) return;
  const shipName = document.getElementById('shipName').value || 'Unnamed ship';
  const ship = findShipByName(shipName) || (currentShipConfig && sameShipName(currentShipConfig.ship_name, shipName) ? currentShipConfig : null);
  if(!ship || !ship.holds || !ship.holds.length) return;
  currentShipConfig = clone(ship);
  selectedShipFile = currentShipConfig._file || selectedShipFile;
  const holdSel = document.getElementById('holdName');
  selectedHoldIndex = Math.max(0, Math.min(holdSel.selectedIndex >= 0 ? holdSel.selectedIndex : 0, currentShipConfig.holds.length-1));
  applyShipToMainForm(currentShipConfig);
  if(closeModal) shipModal.style.display = 'none';
  if(regenerate && document.getElementById('cargoFile').files.length){ document.getElementById('form').requestSubmit(); }
}
function numOrNull(v){ v = String(v || '').replace(',', '.').trim(); return v === '' ? null : Number(v); }
function setVal(id, v){ document.getElementById(id).value = (v ?? ''); }
function cleanHoldName(v, idx){ return (v && String(v).trim()) || `Hold ${idx+1}`; }
function getHoldFromLibraryForm(){
  const shipName = document.getElementById('libShipName').value || 'Unnamed ship';
  return {
    ship_name: shipName,
    hold_name: document.getElementById('libHoldName').value || 'Hold 1',
    hold_length_m: numOrNull(document.getElementById('libHoldLength').value) || 0,
    hold_width_m: numOrNull(document.getElementById('libHoldWidth').value) || 0,
    hold_depth_m: numOrNull(document.getElementById('libHoldDepth').value),
    max_stack_height_m: numOrNull(document.getElementById('libMaxStack').value),
    tank_top_limit_t_m2: numOrNull(document.getElementById('libTankTop').value),
    bilge_radius_m: numOrNull(document.getElementById('libBilge').value),
    hopper_angle_deg: numOrNull(document.getElementById('libHopper').value),
    hatch_opening_width_m: numOrNull(document.getElementById('libHatch').value),
    frame_spacing_m: numOrNull(document.getElementById('libFrame').value),
    coil_diameter_m: numOrNull(document.getElementById('libDiameter').value) || 1.8,
    row_gap_m: numOrNull(document.getElementById('libRowGap').value) || 0.15,
    center_gap_m: numOrNull(document.getElementById('libCenterGap').value) || 0,
    stowage_pattern: stowagePattern.value
  };
}
function syncCurrentHoldFromForm(){
  if(!currentShipConfig.holds) currentShipConfig.holds = [];
  currentShipConfig.ship_name = document.getElementById('libShipName').value || 'Unnamed ship';
  const h = getHoldFromLibraryForm();
  currentShipConfig.holds[selectedHoldIndex] = h;
}
function getShipFromLibraryForm(){
  syncCurrentHoldFromForm();
  currentShipConfig.holds = (currentShipConfig.holds || []).map((h,i)=>({...h, ship_name: currentShipConfig.ship_name, hold_name: cleanHoldName(h.hold_name, i)}));
  return currentShipConfig;
}
function fillHoldForm(s){
  setVal('libHoldName', s.hold_name); setVal('libHoldLength', s.hold_length_m); setVal('libHoldWidth', s.hold_width_m);
  setVal('libHoldDepth', s.hold_depth_m); setVal('libMaxStack', s.max_stack_height_m); setVal('libTankTop', s.tank_top_limit_t_m2);
  setVal('libBilge', s.bilge_radius_m); setVal('libHopper', s.hopper_angle_deg); setVal('libHatch', s.hatch_opening_width_m); setVal('libFrame', s.frame_spacing_m);
  setVal('libDiameter', s.coil_diameter_m ?? 1.8); setVal('libRowGap', s.row_gap_m ?? 0.15); setVal('libCenterGap', s.center_gap_m ?? 0);
}
function renderHoldSelector(){
  const holds = currentShipConfig.holds || [];
  libHoldSelector.innerHTML = holds.map((h,i)=>`<option value="${i}">${h.hold_name || ('Hold '+(i+1))}</option>`).join('');
  libHoldSelector.value = String(selectedHoldIndex);
}
function fillLibraryForm(config){
  if(config.holds){
    currentShipConfig = JSON.parse(JSON.stringify(config));
  } else {
    currentShipConfig = {ship_name: config.ship_name || 'Unnamed ship', holds:[config]};
  }
  if(!currentShipConfig.holds || !currentShipConfig.holds.length){
    currentShipConfig.holds = [{ship_name:currentShipConfig.ship_name, hold_name:'Hold 1', hold_length_m:20, hold_width_m:11.5, coil_diameter_m:1.8, row_gap_m:0.15, center_gap_m:0}];
  }
  selectedHoldIndex = Math.min(selectedHoldIndex, currentShipConfig.holds.length-1);
  setVal('libShipName', currentShipConfig.ship_name);
  renderHoldSelector();
  fillHoldForm(currentShipConfig.holds[selectedHoldIndex]);
}
function applyShipToMainForm(shipOrHold){
  // v5.3: one-way automatic Fleet Library -> Voyage Setup sync.
  // The selected ship/hold in Fleet Library or Voyage Setup is the source; no manual Sync button is required.
  applyingVoyageSync = true;
  try{
    let h;
    let shipName;
    let ship;
    if(shipModal && shipModal.style.display === 'flex'){
      // When Fleet Library is open, copy the visible hold fields and keep the current hold in memory.
      h = getHoldFromLibraryForm();
      shipName = document.getElementById('libShipName').value || (currentShipConfig && currentShipConfig.ship_name) || 'Unnamed ship';
      currentShipConfig.ship_name = shipName;
      if(!currentShipConfig.holds) currentShipConfig.holds = [];
      currentShipConfig.holds[selectedHoldIndex] = {...h, ship_name: shipName};
      ship = currentShipConfig;
    } else {
      ship = shipOrHold && shipOrHold.holds ? shipOrHold : currentShipConfig;
      const holds = ship && ship.holds ? ship.holds : [shipOrHold];
      selectedHoldIndex = Math.max(0, Math.min(selectedHoldIndex || 0, (holds.length || 1)-1));
      h = holds[selectedHoldIndex] || holds[0] || {};
      shipName = (ship && ship.ship_name) || h.ship_name || 'Unnamed ship';
    }

    ensureMainShipDropdown(shipName);
    document.getElementById('shipName').value = shipName;
    renderVoyageHoldDropdown(ship, selectedHoldIndex);

    setVal('holdWidth', h.hold_width_m ?? 11.5);
    setVal('holdLength', h.hold_length_m ?? 20);
    setVal('stowageLength', h.stowage_length_m ?? h.hold_length_m ?? 20);
    setVal('coilDiameter', h.coil_diameter_m ?? 1.8);
    setVal('rowGap', h.row_gap_m ?? 0.15);
    setVal('centerGap', h.center_gap_m ?? 0);
    setVal('maxStackHeight', h.max_stack_height_m);
    setVal('tankTopLimit', h.tank_top_limit_t_m2);

    document.getElementById('form').dataset.shipConfig = JSON.stringify({ship_name: shipName, hold: h, hold_index:selectedHoldIndex});
    if(h.stowage_pattern){ stowagePattern.value = h.stowage_pattern; }
    updatePatternUI();
    ['holdWidth','holdLength','stowageLength','coilDiameter','rowGap','centerGap','maxStackHeight','tankTopLimit'].forEach(id => {
      const el = document.getElementById(id);
      if(el){
        el.dispatchEvent(new Event('input', {bubbles:true}));
        el.dispatchEvent(new Event('change', {bubbles:true}));
      }
    });
  } finally {
    applyingVoyageSync = false;
  }
  const ship = currentShipConfig;
  const h = (ship && ship.holds && ship.holds[selectedHoldIndex]) || {};
  return h;
}
function voyageSetupAsShip(){
  const name = document.getElementById('shipName').value || 'Unnamed ship';
  const holdNameValue = document.getElementById('holdName').value || 'Hold 1';
  return {ship_name:name, holds:[{ship_name:name, hold_name:holdNameValue, hold_length_m:numOrNull(document.getElementById('holdLength').value), stowage_length_m:numOrNull(document.getElementById('stowageLength').value), hold_width_m:numOrNull(document.getElementById('holdWidth').value), coil_diameter_m:numOrNull(document.getElementById('coilDiameter').value), row_gap_m:numOrNull(document.getElementById('rowGap').value), center_gap_m:numOrNull(document.getElementById('centerGap').value), max_stack_height_m:numOrNull(document.getElementById('maxStackHeight').value), tank_top_limit_t_m2:numOrNull(document.getElementById('tankTopLimit').value), stowage_pattern:stowagePattern.value}]};
}
function selectSavedShip(s, holdIndex=0){
  selectedShipFile = s._file || selectedShipFile;
  selectedHoldIndex = Math.max(0, Math.min(holdIndex, ((s.holds || []).length || 1) - 1));
  fillLibraryForm(JSON.parse(JSON.stringify(s)));
  const h = applyShipToMainForm(currentShipConfig);
  shipListBox.querySelectorAll('.shipItem').forEach(x=>x.classList.toggle('active', x.dataset.file === selectedShipFile));
  shipLibraryStatus.textContent = `Loaded to Voyage Setup: ${currentShipConfig.ship_name || 'Unnamed ship'} - ${h.hold_name || 'Hold 1'}`;
}
async function refreshShipLibrary({keepSelection=true} = {}){
  shipListBox.innerHTML = 'Loading...';
  let apiShips = [];
  try {
    const r = await fetch('/api/ships', {cache:'no-store'});
    const data = await r.json();
    apiShips = data.ships || [];
  } catch(e) { apiShips = []; }
  savedShips = mergeFleet(apiShips, localFleet());
  ensureMainShipDropdown(document.getElementById('shipName').value);
  if(!savedShips.length){ shipListBox.innerHTML = '<div class="details">No saved ships yet.</div>'; return; }
  shipListBox.innerHTML = savedShips.map((s,i)=>`<div class="shipItem ${s._file===selectedShipFile?'active':''}" data-i="${i}" data-file="${s._file || ''}"><b>${s.ship_name || 'Unnamed ship'}</b><span>${(s.holds||[]).length} hold(s)</span></div>`).join('');
  shipListBox.querySelectorAll('.shipItem').forEach(item => item.addEventListener('click', () => {
    const s = savedShips[Number(item.dataset.i)];
    selectSavedShip(s, 0);
  }));
  if(keepSelection && selectedShipFile){
    const active = savedShips.find(s => s._file === selectedShipFile);
    if(active) selectSavedShip(active, selectedHoldIndex);
  }
}
shipLibraryTool.addEventListener('click', async () => {
  shipModal.style.display = 'flex';
  if(!selectedShipFile){ selectedHoldIndex = 0; fillLibraryForm(voyageSetupAsShip()); }
  await refreshShipLibrary({keepSelection:true});
});
closeShipModal.addEventListener('click', () => shipModal.style.display = 'none');
document.getElementById('refreshShips').addEventListener('click', refreshShipLibrary);
libHoldSelector.addEventListener('change', () => {
  syncCurrentHoldFromForm();
  selectedHoldIndex = Number(libHoldSelector.value);
  fillHoldForm(currentShipConfig.holds[selectedHoldIndex]);
  upsertLocalShip(currentShipConfig);
  const h = applyShipToMainForm(currentShipConfig);
  shipLibraryStatus.textContent = `Auto-synced to Voyage Setup: ${currentShipConfig.ship_name || 'Unnamed ship'} - ${h.hold_name || 'Hold ' + (selectedHoldIndex+1)}`;
});
document.getElementById('addHoldBtn').addEventListener('click', () => { syncCurrentHoldFromForm(); selectedHoldIndex = currentShipConfig.holds.length; currentShipConfig.holds.push({...currentShipConfig.holds[0], hold_name:`Hold ${selectedHoldIndex+1}`}); renderHoldSelector(); fillHoldForm(currentShipConfig.holds[selectedHoldIndex]); shipLibraryStatus.textContent='Hold added. Press SAVE SHIP.'; });
document.getElementById('deleteHoldBtn').addEventListener('click', () => { if((currentShipConfig.holds||[]).length<=1){ shipLibraryStatus.textContent='A ship must have at least one hold.'; return; } currentShipConfig.holds.splice(selectedHoldIndex,1); selectedHoldIndex=0; renderHoldSelector(); fillHoldForm(currentShipConfig.holds[0]); shipLibraryStatus.textContent='Hold removed. Press SAVE SHIP.'; });
document.getElementById('newShipBtn').addEventListener('click', () => { selectedShipFile = null; selectedHoldIndex=0; fillLibraryForm({ship_name:'New ship', holds:[{ship_name:'New ship', hold_name:'Hold 1', hold_length_m:20, hold_width_m:11.5, coil_diameter_m:1.8, row_gap_m:0.15, center_gap_m:0, stowage_pattern:'auto_width_wedge'}]}); shipLibraryStatus.textContent='New ship template.'; });
document.getElementById('saveShipBtn').addEventListener('click', async () => {
  const ship = getShipFromLibraryForm();
  if(selectedShipFile) ship._file = selectedShipFile;
  const r = await fetch('/api/ships', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(ship)});
  const data = await r.json(); if(!r.ok){ shipLibraryStatus.textContent = data.detail || 'Save failed'; return; }
  selectedShipFile = data.file; currentShipConfig = data.ship; upsertLocalShip(currentShipConfig); applyShipToMainForm(currentShipConfig); shipLibraryStatus.textContent = `Saved and auto-synced to Voyage Setup: ${ship.ship_name} (${ship.holds.length} hold(s))`; await refreshShipLibrary();
});
document.getElementById('loadShipBtn').addEventListener('click', () => {
  const ship = getShipFromLibraryForm();
  const saved = upsertLocalShip(ship);
  currentShipConfig = clone(saved);
  ensureMainShipDropdown(currentShipConfig.ship_name);
  applyShipToMainForm(currentShipConfig);
  const h = currentShipConfig.holds[selectedHoldIndex] || currentShipConfig.holds[0];
  shipLibraryStatus.textContent = `AUTO-SYNCED: ${ship.ship_name || 'Unnamed ship'} - ${h.hold_name || 'Hold 1'} (${h.hold_length_m} m x ${h.hold_width_m} m)`;
  shipModal.style.display = 'none';
});

document.getElementById('shipName').addEventListener('change', () => {
  if(applyingVoyageSync) return;
  const ship = findShipByName(document.getElementById('shipName').value);
  if(ship){
    currentShipConfig = clone(ship);
    selectedShipFile = currentShipConfig._file || selectedShipFile;
    selectedHoldIndex = 0;
    applyShipToMainForm(currentShipConfig);
    renderAllocationSummary();
    autoGeneratePlan(300);
  }
});
document.getElementById('holdName').addEventListener('change', () => {
  if(applyingVoyageSync) return;
  const ship = findShipByName(document.getElementById('shipName').value) || currentShipConfig;
  if(ship && ship.holds && ship.holds.length){
    currentShipConfig = clone(ship);
    selectedHoldIndex = Math.max(0, document.getElementById('holdName').selectedIndex);
    applyShipToMainForm(currentShipConfig);
    renderAllocationSummary();
    autoGeneratePlan(300);
  }
});

document.getElementById('deleteShipBtn').addEventListener('click', async () => {
  if(!selectedShipFile){ shipLibraryStatus.textContent = 'Select a ship first.'; return; }
  const r = await fetch('/api/ships/' + encodeURIComponent(selectedShipFile), {method:'DELETE'}); const data = await r.json();
  const lf = localFleet().filter(s => s._file !== selectedShipFile); saveLocalFleet(lf);
  shipLibraryStatus.textContent = r.ok ? `Deleted: ${selectedShipFile}` : (data.detail || 'Delete failed'); selectedShipFile = null; await refreshShipLibrary();
});
function updateAutoWidthFields(){
  const W = numOrNull(document.getElementById('holdWidth').value) || 0;
  const D = numOrNull(document.getElementById('coilDiameter').value) || 0;
  if(W>0 && D>0){
    let bottom = Math.floor(W / D + 1e-9);
    let gap = W - bottom * D;
    if(gap < 0){ bottom = Math.max(0,bottom-1); gap = W - bottom * D; }
    const port = Math.ceil(bottom / 2), stbd = bottom - port;
    const upper = Math.max(port-1,0) + Math.max(stbd-1,0);
    const wedgeCount = gap > D/3 ? 2 : 1;
    document.getElementById('centerGap').value = gap.toFixed(2);
    const hint = document.getElementById('autoGapHint');
    if(hint) hint.textContent = `Auto: ${bottom} bottom coils (${port}+${stbd}), central gap ${gap.toFixed(2)} m. ${wedgeCount} wedge coil(s) recommended.`;
    if(stowagePattern.value === 'builder'){
      builderPort.value = String(port); builderStbd.value = String(stbd); builderUpper.value = String(upper);
    }
  }
}

function clampStowageLength(){
  const holdLen = numOrNull(document.getElementById('holdLength').value) || 0;
  const el = document.getElementById('stowageLength');
  let stowLen = numOrNull(el.value);
  if(stowLen === null || stowLen <= 0){ return; }
  if(holdLen > 0 && stowLen > holdLen){ el.value = holdLen.toFixed(2); }
}
function estimatePatternCapacity(){
  const W = numOrNull(document.getElementById('holdWidth').value) || 0;
  const D = numOrNull(document.getElementById('coilDiameter').value) || 0;
  if(!(W>0 && D>0)) return 0;
  let bottom = Math.floor(W / D + 1e-9);
  let gap = W - bottom * D;
  if(gap < 0){ bottom = Math.max(0, bottom-1); gap = W - bottom * D; }
  const port = Math.ceil(bottom / 2), stbd = bottom - port;
  const upper = Math.max(port-1,0) + Math.max(stbd-1,0);
  const wedgeCount = gap > D/3 ? 2 : 1;
  return bottom + upper + wedgeCount;
}
function allocationBase(){
  const totalCoils = Number((lastCargoPreview && lastCargoPreview.coil_count) || (lastPlanData && lastPlanData.coil_count) || 0);
  const totalWeight = Number((lastCargoPreview && lastCargoPreview.total_weight_t) || (lastPlanData && lastPlanData.total_weight_t) || 0);
  const avgW = Number((lastCargoPreview && (lastCargoPreview.avg_width_m || lastCargoPreview.max_width_m)) || 0);
  const avgT = totalCoils ? totalWeight / totalCoils : 0;
  return {totalCoils,totalWeight,avgW,avgT};
}
function capacityForHold(h){
  const W = Number(h.hold_width_m || h.width_m || numOrNull(document.getElementById('holdWidth').value) || 0);
  const D = Number(h.coil_diameter_m || h.diameter_m || numOrNull(document.getElementById('coilDiameter').value) || 0);
  if(!(W>0 && D>0)) return estimatePatternCapacity();
  let bottom = Math.floor(W / D + 1e-9);
  let gap = W - bottom * D;
  if(gap < 0){ bottom = Math.max(0,bottom-1); gap = W - bottom * D; }
  const port = Math.ceil(bottom / 2), stbd = bottom - port;
  const upper = Math.max(port-1,0) + Math.max(stbd-1,0);
  const wedgeCount = gap > D/3 ? 2 : 1;
  return bottom + upper + wedgeCount;
}
function lengthForBlocks(blocks, avgW, rowGap){
  blocks = Math.max(0, Math.floor(blocks || 0));
  return blocks ? blocks * avgW + Math.max(0, blocks-1) * rowGap : 0;
}
function blocksForLength(len, avgW, rowGap){
  if(!(len>0 && avgW>0)) return 0;
  return Math.max(0, Math.floor((len + rowGap + 1e-9) / (avgW + rowGap)));
}

let autoPlanTimer = null;
function hasCargoFile(){
  const f = document.getElementById('cargoFile');
  return !!(f && f.files && f.files.length);
}
function autoGeneratePlan(delay=350){
  if(!hasCargoFile()) return;
  clearTimeout(autoPlanTimer);
  autoPlanTimer = setTimeout(() => {
    const formEl = document.getElementById('form');
    if(formEl) formEl.requestSubmit();
  }, delay);
}
function persistActiveHoldStowage(len){
  const ship = activeFleetShip();
  if(!(ship && ship.holds && ship.holds.length)) return;
  const idx = Math.max(0, Math.min(document.getElementById('holdName').selectedIndex >= 0 ? document.getElementById('holdName').selectedIndex : selectedHoldIndex, ship.holds.length-1));
  const working = clone(ship);
  working.holds[idx] = {...working.holds[idx], stowage_length_m: Number(len)||0};
  currentShipConfig = clone(working);
  upsertLocalShip(currentShipConfig);
}
function activeFleetShip(){
  return findShipByName(document.getElementById('shipName').value) || currentShipConfig || null;
}
function computeHoldAllocations(commitNext=false){
  const base = allocationBase();
  const ship = activeFleetShip();
  const holds = (ship && ship.holds && ship.holds.length) ? clone(ship.holds) : [{hold_name:document.getElementById('holdName').value || 'Hold 1', hold_length_m:numOrNull(document.getElementById('holdLength').value) || 0, hold_width_m:numOrNull(document.getElementById('holdWidth').value) || 0, coil_diameter_m:numOrNull(document.getElementById('coilDiameter').value) || 0, row_gap_m:numOrNull(document.getElementById('rowGap').value) || 0}];
  const startIdx = Math.max(0, Math.min(document.getElementById('holdName').selectedIndex >= 0 ? document.getElementById('holdName').selectedIndex : selectedHoldIndex, holds.length-1));
  const rowGap = numOrNull(document.getElementById('rowGap').value) || 0;
  const manualLen = numOrNull(document.getElementById('stowageLength').value) || numOrNull(document.getElementById('holdLength').value) || 0;
  let remaining = base.totalCoils;
  const allocations = holds.map((h,i) => ({idx:i, name:h.hold_name || `Hold ${i+1}`, length:0, blocks:0, coils:0, tonnes:0, capacity:capacityForHold(h), maxLen:Number(h.hold_length_m || h.length_m || 0)}));
  if(!(base.totalCoils>0 && base.avgW>0)){ return {allocations, remainingCoils:0, remainingTonnes:0, totalLength:0, totalWeight:0, base}; }
  for(let i=0; i<allocations.length; i++){
    const a = allocations[i];
    const h = holds[i] || {};
    const maxLen = a.maxLen || (i===startIdx ? numOrNull(document.getElementById('holdLength').value) || 0 : 0);
    let len;
    if(i < startIdx){
      len = Math.max(0, Math.min(maxLen, Number(h.stowage_length_m || 0)));
    } else if(i === startIdx){
      len = Math.max(0, Math.min(maxLen || manualLen, manualLen));
    } else {
      // v7.0 Allocation Workspace: after the active hold, allocate the remaining cargo automatically.
      // Do not keep stale saved lengths for following holds; they must follow the marker live.
      const needBlocks = a.capacity ? Math.ceil(remaining / a.capacity) : 0;
      len = Math.min(maxLen, lengthForBlocks(needBlocks, base.avgW, rowGap));
    }
    const blocks = blocksForLength(len, base.avgW, rowGap);
    const coils = Math.min(remaining, blocks * (a.capacity || 0));
    a.length = Number(len.toFixed(2));
    a.blocks = blocks;
    a.coils = coils;
    a.tonnes = coils * base.avgT;
    remaining = Math.max(0, remaining - coils);
    if(commitNext && i >= startIdx){
      holds[i].stowage_length_m = a.length;
    }
  }
  if(commitNext && ship && ship.holds){
    ship.holds = holds;
    currentShipConfig = clone(ship);
    upsertLocalShip(currentShipConfig);
  }
  const totalLength = allocations.reduce((s,a)=>s+a.length,0);
  const totalWeight = allocations.reduce((s,a)=>s+a.tonnes,0);
  return {allocations, remainingCoils:remaining, remainingTonnes:remaining*base.avgT, totalLength, totalWeight, base};
}
function allocationHtml(){
  const r = computeHoldAllocations(false);
  if(!r.base.totalCoils || !r.base.avgW) return '<div class="details"><b>Allocation Workspace</b><br>Import cargo and build a plan to see live hold-by-hold length, coils and weight.</div>';
  const selected = Math.max(0, document.getElementById('holdName').selectedIndex);
  const remainingClass = r.remainingCoils > 0 ? 'bad' : 'ok';
  const rows = r.allocations.map(a => `<tr class="${a.idx===selected ? 'activeAllocRow':''}"><td>${a.name}</td><td>${a.length.toFixed(2)} m</td><td>${a.blocks}</td><td>${a.coils}</td><td>${a.tonnes.toFixed(1)} t</td></tr>`).join('');
  return `<div class="stats" style="margin-bottom:10px">
      <div class="stat"><b>Total allocated</b><span>${r.totalWeight.toFixed(1)} t</span></div>
      <div class="stat"><b>Length used</b><span>${r.totalLength.toFixed(2)} m</span></div>
      <div class="stat"><b>Remaining coils</b><span class="${remainingClass}">${r.remainingCoils}</span></div>
      <div class="stat"><b>Remaining weight</b><span class="${remainingClass}">${r.remainingTonnes.toFixed(1)} t</span></div>
    </div>
    <table><thead><tr><th>Hold</th><th>Length</th><th>Blocks</th><th>Coils</th><th>Weight</th></tr></thead><tbody>${rows}</tbody></table>
    <div class="hint">Move the red marker. Allocation updates live; following holds receive the remaining cargo automatically.</div>`;
}
function renderAllocationSummary(){
  const html = allocationHtml();
  const box = document.getElementById('allocationPanel');
  if(box) box.innerHTML = html;
  const ws = document.getElementById('allocationWorkspace');
  if(ws) ws.innerHTML = html;
}
function commitAllocationToNextHolds({regenerate=false}={}){
  const len = numOrNull(document.getElementById('stowageLength').value) || 0;
  persistActiveHoldStowage(len);
  computeHoldAllocations(true);
  renderAllocationSummary();
  updateAllocationHint();
  if(regenerate) autoGeneratePlan(250);
}
function updateAllocationHint(){
  const hint = document.getElementById('allocationHint');
  if(!hint) return;
  const holdLen = numOrNull(document.getElementById('holdLength').value) || 0;
  const stowLen = numOrNull(document.getElementById('stowageLength').value) || holdLen;
  const rowGap = numOrNull(document.getElementById('rowGap').value) || 0;
  const cap = estimatePatternCapacity();
  if(!lastCargoPreview){
    hint.textContent = `Use stowage length: ${stowLen.toFixed(2)} m of ${holdLen.toFixed(2)} m. Import cargo to estimate coils/tonnes and remaining cargo for the next hold.`;
    return;
  }
  const avgW = Number(lastCargoPreview.avg_width_m || lastCargoPreview.max_width_m || 0);
  const avgT = Number(lastCargoPreview.avg_weight_t || (lastCargoPreview.total_weight_t / Math.max(lastCargoPreview.coil_count,1)) || 0);
  if(!(avgW>0 && cap>0)){
    hint.textContent = `Use stowage length: ${stowLen.toFixed(2)} m of ${holdLen.toFixed(2)} m.`;
    return;
  }
  const blocks = Math.max(0, Math.floor((stowLen + rowGap) / (avgW + rowGap)));
  const coils = Math.min(lastCargoPreview.coil_count, blocks * cap);
  const tonnes = coils * avgT;
  const remCoils = Math.max(0, lastCargoPreview.coil_count - coils);
  const remTonnes = Math.max(0, lastCargoPreview.total_weight_t - tonnes);
  const remBlocks = cap ? Math.ceil(remCoils / cap) : 0;
  const remLen = remBlocks ? remBlocks * avgW + Math.max(0, remBlocks-1) * rowGap : 0;
  hint.textContent = `This hold: approx. ${blocks} blocks / ${coils} coils / ${tonnes.toFixed(1)} t. Remaining for next hold: ${remCoils} coils / ${remTonnes.toFixed(1)} t, approx. ${remLen.toFixed(2)} m. Press Enter to commit remaining cargo to next hold(s).`;
  renderAllocationSummary();
}

function buildPatternText(){
  const p = parseInt(builderPort.value || '0', 10);
  const s = parseInt(builderStbd.value || '0', 10);
  let u = parseInt(builderUpper.value || '0', 10);
  // Wedge rule: upper tier is automatically one fewer than bottom on each side.
  if(builderWedge.value === 'yes' && p > 0 && s > 0){
    u = Math.max(p - 1, 0) + Math.max(s - 1, 0);
    builderUpper.value = String(u);
  }
  let parts = [];
  if(p > 0 && s > 0) parts.push(`${p}+${s}`);
  else if(p + s > 0) parts.push(`${p+s}`);
  if(builderWedge.value === 'yes') parts.push('Wedge');
  if(u > 0) parts.push(`${u}`);
  return parts.join(' / ') || 'Custom / Manual';
}
function updatePatternUI(){
  updateAutoWidthFields();
  const isCustom = stowagePattern.value === 'custom';
  const isBuilder = stowagePattern.value === 'builder';
  customPatternBox.style.display = isCustom ? 'block' : 'none';
  builderBox.style.display = isBuilder ? 'block' : 'none';
  const built = buildPatternText();
  builderPattern.value = built;
  builderPreview.textContent = `Builder pattern: ${built}`;
  if(isCustom) activePatternTool.textContent = customPattern.value || 'Custom / Manual';
  else if(isBuilder) activePatternTool.textContent = built;
  else activePatternTool.textContent = stowagePattern.options[stowagePattern.selectedIndex].text;
  updateAllocationHint();
}
stowagePattern.addEventListener('change', updatePatternUI);
document.getElementById('holdWidth').addEventListener('input', () => { updatePatternUI(); updateAllocationHint(); });
document.getElementById('holdLength').addEventListener('input', () => { clampStowageLength(); updateAllocationHint(); });
document.getElementById('stowageLength').addEventListener('input', () => { clampStowageLength(); updateAllocationHint(); renderAllocationSummary(); });
document.getElementById('stowageLength').addEventListener('change', () => { commitAllocationToNextHolds({regenerate:true}); });
document.getElementById('rowGap').addEventListener('input', updateAllocationHint);
document.getElementById('coilDiameter').addEventListener('input', () => { updatePatternUI(); updateAllocationHint(); });
customPattern.addEventListener('input', updatePatternUI);
[builderPort,builderStbd,builderWedge,builderUpper].forEach(el => el.addEventListener('input', updatePatternUI));
[builderWedge].forEach(el => el.addEventListener('change', updatePatternUI));
updatePatternUI();
document.getElementById('autoOptimizeTool').addEventListener('click', () => alert('Auto Optimize will be implemented after the geometry engine is tested.'));
document.getElementById('reportsTool').addEventListener('click', () => alert('Reports will be implemented after generated plans are tested.'));
document.getElementById('cargoFile').addEventListener('change', e => {
  uploadState.textContent = e.target.files[0] ? e.target.files[0].name : 'No file';
});


function svgEl(parent, name, attrs){
  const ns = 'http://www.w3.org/2000/svg';
  const e = document.createElementNS(ns, name);
  Object.entries(attrs || {}).forEach(([k,v]) => e.setAttribute(k,v));
  parent.appendChild(e);
  return e;
}
function clearSvg(target){ target.innerHTML = ''; target.setAttribute('viewBox','0 0 1000 600'); }
function selectView(view){
  currentView = view;
  viewTabs.forEach(b => b.classList.toggle('active', b.dataset.view === view));
  planTitle.textContent = view === 'top' ? 'Hold Plan – Top View' : view === 'section' ? 'Hold Plan – Cross Section' : 'Hold Plan – 3D View';
  svg.style.display = 'none'; sectionSvg.style.display = 'none'; threeDSvg.style.display = 'none'; threeDNote.style.display = 'none';
  if(!lastPlanData){ return; }
  emptyPlan.style.display = 'none'; legend.style.display = 'block';
  if(view === 'top'){ svg.style.display = 'block'; }
  if(view === 'section'){ drawSectionView(lastPlanData); sectionSvg.style.display = 'block'; }
  if(view === '3d'){ draw3DView(lastPlanData); threeDSvg.style.display = 'block'; threeDNote.style.display = 'block'; }
}
viewTabs.forEach(b => b.addEventListener('click', () => selectView(b.dataset.view)));
document.addEventListener('keydown', (evt) => {
  if(evt.key === 'Enter' && lastPlanData && currentView === 'top'){
    const tag = String((evt.target && evt.target.tagName) || '').toLowerCase();
    if(tag !== 'textarea'){
      commitAllocationToNextHolds();
    }
  }
});

function drawSectionView(data){
  const coils = data.coils || [];
  const hold = data.hold || {width_m:11.5, diameter_m:1.8};
  clearSvg(sectionSvg);
  const pad = 55, W = 1000, H = 600;
  const maxZ = Math.max(hold.diameter_m * 2.8, ...coils.map(c => (Number(c.z_m)||0) + (Number(c.Diameter_m)||hold.diameter_m)/2 + 0.3));
  const scale = Math.min((W-pad*2)/hold.width_m, (H-pad*2)/maxZ);
  const baseY = H - pad;
  svgEl(sectionSvg,'rect',{x:pad,y:baseY-maxZ*scale,width:hold.width_m*scale,height:maxZ*scale,fill:'#ffffff',stroke:'#0f172a','stroke-width':2,rx:6});
  svgEl(sectionSvg,'line',{x1:pad,y1:baseY,x2:pad+hold.width_m*scale,y2:baseY,stroke:'#0f172a','stroke-width':3});
  for(let y=0; y<=hold.width_m; y+=1){
    const xx = pad + y*scale;
    svgEl(sectionSvg,'line',{x1:xx,y1:baseY-maxZ*scale,x2:xx,y2:baseY,stroke:'#e2e8f0','stroke-width':1});
  }
  const firstBlock = Math.min(...coils.map(c => Number(c.Block)||1));
  const sample = coils.filter(c => Number(c.Block) === firstBlock);
  sample.forEach(c => {
    const d = Number(c.Diameter_m)||hold.diameter_m;
    const r = d/2*scale;
    const cx = pad + Number(c.y_m)*scale;
    const cy = baseY - Number(c.z_m)*scale;
    const circ = svgEl(sectionSvg,'circle',{cx,cy,r,fill:coilColor(c),stroke:'#0f172a','stroke-width':2,opacity:.9,style:'cursor:pointer'});
    circ.addEventListener('click', () => showCoilDetails(c));
    const txt = svgEl(sectionSvg,'text',{x:cx,y:cy+4,fill:'#fff','font-size':12,'font-weight':800,'text-anchor':'middle','pointer-events':'none'});
    txt.textContent = c.Position;
  });
  const title = svgEl(sectionSvg,'text',{x:pad,y:32,fill:'#0f172a','font-size':15,'font-weight':800});
  title.textContent = `Cross section: Block ${firstBlock} · Hold width ${hold.width_m.toFixed(2)} m`;
}

function isoProject(x,y,z){
  const sx = 95 + (x*30) + (y*42);
  const sy = 460 + (x*16) - (y*18) - (z*44);
  return [sx, sy];
}
function drawIsoCylinder(c, hold){
  const d = Number(c.Diameter_m)||hold.diameter_m;
  const x0 = Number(c.x0_m), x1 = Number(c.x1_m), y = Number(c.y_m), z = Number(c.z_m);
  const r = d/2;
  const [aX,aY] = isoProject(x0,y,z);
  const [bX,bY] = isoProject(x1,y,z);
  const length = Math.max(10, Math.hypot(bX-aX,bY-aY));
  const angle = Math.atan2(bY-aY,bX-aX) * 180 / Math.PI;
  const g = svgEl(threeDSvg,'g',{transform:`translate(${aX} ${aY}) rotate(${angle})`,style:'cursor:pointer'});
  const color = coilColor(c);
  const body = svgEl(g,'rect',{x:0,y:-8,width:length,height:16,rx:8,fill:color,stroke:'#0f172a','stroke-width':1,opacity:.88});
  svgEl(g,'ellipse',{cx:0,cy:0,rx:8,ry:8,fill:color,stroke:'#0f172a','stroke-width':1});
  svgEl(g,'ellipse',{cx:length,cy:0,rx:8,ry:8,fill:'#ffffff',stroke:'#0f172a','stroke-width':1,opacity:.45});
  g.addEventListener('click', () => showCoilDetails(c));
}
function draw3DView(data){
  const coils = data.coils || [];
  const hold = data.hold || {length_m:20,width_m:11.5,diameter_m:1.8};
  clearSvg(threeDSvg);
  const corners = [[0,0,0],[hold.length_m,0,0],[hold.length_m,hold.width_m,0],[0,hold.width_m,0]];
  const pts = corners.map(p => isoProject(...p));
  svgEl(threeDSvg,'polygon',{points:pts.map(p=>p.join(',')).join(' '),fill:'#ffffff',stroke:'#0f172a','stroke-width':2,opacity:.95});
  for(let x=0; x<=hold.length_m; x+=2){
    const p1=isoProject(x,0,0), p2=isoProject(x,hold.width_m,0);
    svgEl(threeDSvg,'line',{x1:p1[0],y1:p1[1],x2:p2[0],y2:p2[1],stroke:'#e2e8f0','stroke-width':1});
  }
  const sorted = [...coils].sort((a,b)=> (Number(a.z_m)-Number(b.z_m)) || (Number(a.y_m)-Number(b.y_m)) || (Number(a.x0_m)-Number(b.x0_m)) );
  sorted.forEach(c => drawIsoCylinder(c, hold));
  const title = svgEl(threeDSvg,'text',{x:45,y:32,fill:'#0f172a','font-size':15,'font-weight':800});
  title.textContent = `3D beta · ${coils.length} coils · ${data.total_weight_t.toFixed(1)} t`;
}
function showCoilDetails(c){
  coilDetails.innerHTML = `
    <b>ID:</b> ${c.ID}<br>
    <b>Block:</b> ${c.Block} · <b>Position:</b> ${c.Position} · <b>Tier:</b> ${c.Tier}<br>
    <b>Width:</b> ${Number(c.Width_m).toFixed(3)} m<br>
    <b>Weight:</b> ${Number(c.Weight_t).toFixed(3)} t<br>
    ${c.Diameter_m ? `<b>Diameter:</b> ${Number(c.Diameter_m).toFixed(3)} m<br>` : ``}
    <b>X:</b> ${Number(c.x0_m).toFixed(2)}–${Number(c.x1_m).toFixed(2)} m · <b>Y:</b> ${Number(c.y_m).toFixed(2)} m · <b>Z:</b> ${Number(c.z_m || 0).toFixed(2)} m
  `;
}

function tierColor(tier){
  if(tier === 'Bottom') return '#16a34a';  // Tier 1
  if(tier === 'Wedge') return '#facc15';  // wedge, also tier 2 support
  if(tier === 'Center') return '#facc15';
  return '#2563eb';                       // Tier 2
}
function weightColor(w){
  w = Number(w)||0;
  if(w < 16) return '#16a34a';
  if(w < 22) return '#ca8a04';
  if(w < 28) return '#ea580c';
  return '#dc2626';
}
function coilColor(c){ if(c.Out_of_hold) return '#dc2626'; return tierColor(c.Tier); }
function addTooltip(el, c){
  const title = document.createElementNS('http://www.w3.org/2000/svg','title');
  title.textContent = `${c.ID} · ${Number(c.Weight_t).toFixed(1)} t · ${Number(c.Width_m).toFixed(2)} m · ${c.Tier} ${c.Position}`;
  el.appendChild(title);
}

function svgPointFromEvent(svgNode, evt){
  const pt = svgNode.createSVGPoint();
  pt.x = evt.clientX; pt.y = evt.clientY;
  return pt.matrixTransform(svgNode.getScreenCTM().inverse());
}
function blockSnapLengths(data){
  const coils = data.coils || [];
  const hold = data.hold || {};
  const physical = Number(hold.physical_length_m || hold.length_m || 0);
  const ends = [...new Set(coils.map(c => Number(c.block_x1_m || c.x1_m || 0)).filter(v => v>0 && v<=physical+1e-9).map(v => Number(v.toFixed(3))))].sort((a,b)=>a-b);
  if(!ends.length && lastCargoPreview){
    const cap = estimatePatternCapacity();
    const avgW = Number(lastCargoPreview.avg_width_m || lastCargoPreview.max_width_m || 0);
    const gap = numOrNull(document.getElementById('rowGap').value) || 0;
    if(cap>0 && avgW>0){
      let x = avgW, out=[];
      while(x <= physical + 1e-9){ out.push(Number(x.toFixed(3))); x += avgW + gap; }
      return out;
    }
  }
  return ends;
}
function closestSnap(value, snaps, maxLen){
  if(!snaps || !snaps.length) return Math.max(0, Math.min(maxLen, value));
  let best = snaps[0], dist = Math.abs(value - best);
  for(const s of snaps){ const d = Math.abs(value-s); if(d < dist){ best=s; dist=d; } }
  return Math.max(0, Math.min(maxLen, best));
}
function updateStowageFromMarker(len, data, liveOnly=false){
  const holdLen = Number((data.hold && (data.hold.physical_length_m || data.hold.length_m)) || numOrNull(document.getElementById('holdLength').value) || 0);
  len = Math.max(0, Math.min(holdLen, Number(len)||0));
  const el = document.getElementById('stowageLength');
  el.value = len.toFixed(2);
  persistActiveHoldStowage(len);
  updateAllocationHint();
  const label = document.getElementById('markerReadout');
  if(label) label.textContent = `Stowage marker: ${len.toFixed(2)} m`;
  renderAllocationSummary();
}

function drawInteractivePlan(data){
  const coils = data.coils || [];
  const hold = data.hold || {length_m:20, width_m:11.5};
  const pad = 45;
  const W = 1000, H = 600;
  const physicalPlanLength = Number(hold.physical_length_m || hold.length_m || 20);
  const scaleX = (W - pad*2) / physicalPlanLength;
  const scaleY = (H - pad*2) / hold.width_m;

  svg.innerHTML = '';
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);

  const ns = 'http://www.w3.org/2000/svg';
  function el(name, attrs){
    const e = document.createElementNS(ns, name);
    Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k,v));
    svg.appendChild(e);
    return e;
  }

  // hold rectangle
  el('rect', {x:pad, y:pad, width:physicalPlanLength*scaleX, height:hold.width_m*scaleY, fill:'#ffffff', stroke:'#0f172a', 'stroke-width':2, rx:6});

  // grid every 1 m
  for(let x=0; x<=physicalPlanLength; x+=1){
    el('line', {x1:pad+x*scaleX, y1:pad, x2:pad+x*scaleX, y2:pad+hold.width_m*scaleY, stroke:'#e2e8f0', 'stroke-width':1});
  }
  for(let y=0; y<=hold.width_m; y+=1){
    el('line', {x1:pad, y1:pad+y*scaleY, x2:pad+hold.length_m*scaleX, y2:pad+y*scaleY, stroke:'#e2e8f0', 'stroke-width':1});
  }

  // loaded/free shading controlled by the stowage marker
  const physicalLen = Number(hold.physical_length_m || hold.length_m || 0);
  const stowInputLen = numOrNull(document.getElementById('stowageLength').value);
  const activeLen = Math.max(0, Math.min(physicalLen, stowInputLen || Number(hold.stowage_length_m || hold.length_m || 0)));
  if(physicalLen > 0){
    el('rect', {id:'loadedShade', x:pad, y:pad, width:activeLen*scaleX, height:hold.width_m*scaleY, fill:'#dcfce7', opacity:.42, 'pointer-events':'none'});
    el('rect', {id:'freeShade', x:pad+activeLen*scaleX, y:pad, width:Math.max(0,(physicalLen-activeLen)*scaleX), height:hold.width_m*scaleY, fill:'#e5e7eb', opacity:.40, 'pointer-events':'none'});
  }

  // title inside plan
  const title = el('text', {x:pad+10, y:pad-15, fill:'#0f172a', 'font-size':14, 'font-weight':'700'});
  title.textContent = `Hold ${physicalPlanLength.toFixed(2)} m × ${hold.width_m.toFixed(2)} m · selected stowage ${Number(document.getElementById('stowageLength').value || hold.stowage_length_m || hold.length_m).toFixed(2)} m`;

  coils.forEach(c => {
    const x = pad + c.x0_m * scaleX;
    const y = pad + c.y_m * scaleY;
    const w = Math.max(c.Width_m * scaleX, 14);
    const d = Number(c.Diameter_m) || hold.diameter_m || 1.8;
    const h = Math.min(Math.max(d * scaleY * 0.18, 14), 28);
    const color = coilColor(c);
    const g = el('g', {style:'cursor:pointer'});
    const body = document.createElementNS(ns,'rect');
    Object.entries({x:x, y:y-h/2, width:w, height:h, rx:h/2, fill:color, stroke:'#0f172a', 'stroke-width':0.8, opacity:0.9}).forEach(([k,v]) => body.setAttribute(k,v));
    g.appendChild(body);
    const e1 = document.createElementNS(ns,'ellipse');
    Object.entries({cx:x, cy:y, rx:h/2, ry:h/2, fill:color, stroke:'#0f172a', 'stroke-width':0.8}).forEach(([k,v]) => e1.setAttribute(k,v));
    g.appendChild(e1);
    const e2 = document.createElementNS(ns,'ellipse');
    Object.entries({cx:x+w, cy:y, rx:h/2, ry:h/2, fill:'#ffffff', stroke:'#0f172a', 'stroke-width':0.8, opacity:.38}).forEach(([k,v]) => e2.setAttribute(k,v));
    g.appendChild(e2);
    addTooltip(g,c);
    g.addEventListener('click', () => showCoilDetails(c));
    const text = document.createElementNS(ns,'text');
    Object.entries({x:x+w/2, y:y+4, fill:'#ffffff', 'font-size':8, 'font-weight':'700', 'text-anchor':'middle', 'pointer-events':'none'}).forEach(([k,v]) => text.setAttribute(k,v));
    text.textContent = c.Out_of_hold ? '!' : c.Position;
    g.appendChild(text);
  });

  // visible loaded/free zones and drag instruction
  const instrBg = el('rect', {x:pad, y:pad+hold.width_m*scaleY+18, width:Math.min(430, physicalPlanLength*scaleX), height:28, fill:'#fee2e2', stroke:'#dc2626', 'stroke-width':1, rx:6});
  const instr = el('text', {x:pad+10, y:pad+hold.width_m*scaleY+38, fill:'#991b1b', 'font-size':13, 'font-weight':'900'});
  instr.textContent = 'Drag red marker: choose stowage length (snaps to complete blocks)';

  // draggable stowage length marker. It snaps to complete block ends.
  const snapEnds = blockSnapLengths(data);
  let markerLen = closestSnap(numOrNull(document.getElementById('stowageLength').value) || Number(hold.stowage_length_m || hold.length_m || 0), snapEnds, physicalLen || hold.length_m);
  updateStowageFromMarker(markerLen, data, true);
  const markerX = () => pad + markerLen * scaleX;
  const markerGroup = el('g', {style:'cursor:ew-resize; touch-action:none' });
  const markerLine = document.createElementNS(ns,'line');
  Object.entries({x1:markerX(),y1:pad-10,x2:markerX(),y2:pad+hold.width_m*scaleY+10,stroke:'#dc2626','stroke-width':7, 'stroke-linecap':'round'}).forEach(([k,v])=>markerLine.setAttribute(k,v));
  markerGroup.appendChild(markerLine);
  const markerTri = document.createElementNS(ns,'polygon');
  Object.entries({points:`${markerX()-16},${pad-28} ${markerX()+16},${pad-28} ${markerX()},${pad-5}`,fill:'#dc2626',stroke:'#7f1d1d','stroke-width':2}).forEach(([k,v])=>markerTri.setAttribute(k,v));
  markerGroup.appendChild(markerTri);
  const markerText = document.createElementNS(ns,'text');
  Object.entries({id:'markerReadout',x:markerX()+12,y:pad+24,fill:'#991b1b','font-size':16,'font-weight':900,stroke:'#fff','stroke-width':0.4}).forEach(([k,v])=>markerText.setAttribute(k,v));
  markerText.textContent = `Stowage marker: ${markerLen.toFixed(2)} m`;
  markerGroup.appendChild(markerText);
  svg.appendChild(markerGroup);
  function setMarkerFromEvent(evt){
    const pt = svgPointFromEvent(svg, evt);
    const rawLen = (pt.x - pad) / scaleX;
    markerLen = closestSnap(rawLen, snapEnds, physicalLen || hold.length_m);
    const xNow = markerX();
    markerLine.setAttribute('x1', xNow); markerLine.setAttribute('x2', xNow);
    markerTri.setAttribute('points', `${xNow-16},${pad-28} ${xNow+16},${pad-28} ${xNow},${pad-5}`);
    markerText.setAttribute('x', xNow+8);
    const loadedShade = document.getElementById('loadedShade');
    const freeShade = document.getElementById('freeShade');
    if(loadedShade) loadedShade.setAttribute('width', Math.max(0, markerLen*scaleX));
    if(freeShade){ freeShade.setAttribute('x', pad+markerLen*scaleX); freeShade.setAttribute('width', Math.max(0,(physicalLen-markerLen)*scaleX)); }
    updateStowageFromMarker(markerLen, data, true);
  }
  let dragging = false;
  markerGroup.addEventListener('pointerdown', evt => { dragging=true; markerGroup.setPointerCapture(evt.pointerId); setMarkerFromEvent(evt); });
  markerGroup.addEventListener('pointermove', evt => { if(dragging) setMarkerFromEvent(evt); });
  markerGroup.addEventListener('pointerup', evt => { dragging=false; updateStowageFromMarker(markerLen, data, false); commitAllocationToNextHolds({regenerate:false}); });
  markerGroup.addEventListener('pointercancel', () => dragging=false);
  markerGroup.setAttribute('tabindex','0');
  markerGroup.addEventListener('keydown', evt => { if(evt.key === 'Enter'){ evt.preventDefault(); commitAllocationToNextHolds({regenerate:false}); renderAllocationSummary(); } });

  const key = el('text', {x:pad+10, y:H-18, fill:'#0f172a', 'font-size':12, 'font-weight':'700'});
  key.textContent = 'Top View: drag red marker to choose stowage length. Marker snaps to complete blocks; green = loaded, grey = free.';

  lastPlanData = data;
  emptyPlan.style.display = 'none';
  svg.style.display = currentView === 'top' ? 'block' : 'none';
  legend.style.display = 'block';
  if(currentView === 'section') selectView('section');
  if(currentView === '3d') selectView('3d');
}


importBtn.addEventListener('click', async () => {
  const file = document.getElementById('cargoFile').files[0];
  if(!file){ cargoPreviewBox.innerHTML = '<div class="details"><b>Error:</b><br>Please choose a cargo file first.</div>'; return; }
  importBtn.disabled = true;
  importBtn.textContent = 'IMPORTING...';
  cargoPreviewBox.innerHTML = '<div class="details">Reading cargo and converting units...</div>';
  try{
    const fd = new FormData();
    fd.append('cargo_file', file);
    const response = await fetch('/import-cargo', {method:'POST', body:fd});
    const data = await response.json();
    if(!response.ok) throw new Error(data.detail || 'Import failed');
    lastCargoPreview = data;
    const diaHint = document.getElementById('diameterSourceHint');
    if(data.avg_diameter_m){
      document.getElementById('coilDiameter').value = Number(data.avg_diameter_m).toFixed(3);
      if(diaHint) diaHint.textContent = `Diameter source: cargo list average ${Number(data.avg_diameter_m).toFixed(3)} m (max ${Number(data.max_diameter_m).toFixed(3)} m).`;
      updatePatternUI();
    } else {
      if(diaHint) diaHint.textContent = 'No Diameter column found. Enter average diameter manually.';
    }
    const rows = (data.coils || []).slice(0, 20).map(c => `
      <tr><td>${c.ID}</td><td>${Number(c.Weight_t).toFixed(1)}</td><td>${Number(c.Width_m).toFixed(2)}</td><td>${c.Diameter_m ? Number(c.Diameter_m).toFixed(2) : '-'}</td></tr>
    `).join('');
    cargoPreviewBox.innerHTML = `
      <div class="details"><b>${data.filename}</b><br>${data.coil_count} coils · ${data.total_weight_t.toFixed(1)} t<br>Avg width ${data.avg_width_m.toFixed(2)} m · Max width ${data.max_width_m.toFixed(2)} m${data.avg_diameter_m ? ` · Avg diameter ${data.avg_diameter_m.toFixed(2)} m` : ' · Diameter: manual average required'}</div>
      <table><thead><tr><th>ID</th><th>Weight t</th><th>Width m</th><th>Diam. m</th></tr></thead><tbody>${rows}</tbody></table>
    `;
    updateAllocationHint();
    renderAllocationSummary();
  }catch(err){
    cargoPreviewBox.innerHTML = `<div class="details"><b>Error:</b><br>${err.message}</div>`;
  }finally{
    importBtn.disabled = false;
    importBtn.textContent = 'IMPORT CARGO';
  }
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  btn.disabled = true;
  btn.textContent = 'BUILDING PLAN...';
  summaryBox.innerHTML = '<div class="details">Working...</div>';
  weightsBox.innerHTML = '<div class="details">Working...</div>';

  try {
    const fd = new FormData(form);
    const response = await fetch('/calculate', {method:'POST', body:fd});
    const data = await response.json();
    if(!response.ok) throw new Error(data.detail || 'Calculation failed');
    lastPlanData = data;

    summaryBox.innerHTML = `
      <div class="stats">
        <div class="stat"><b>Coils</b><span>${data.coil_count}</span></div>
        <div class="stat"><b>Total weight</b><span>${data.total_weight_t.toFixed(1)} t</span></div>
        <div class="stat"><b>Used</b><span>${data.used_length_m.toFixed(2)} m</span></div>
        <div class="stat"><b>Free</b><span>${data.free_length_m.toFixed(2)} m</span></div><div class="stat"><b>Use</b><span>${(data.used_length_m / data.hold.length_m * 100).toFixed(0)}%</span></div>
        <div class="stat"><b>Blocks</b><span>${data.blocks}</span></div>
        <div class="stat"><b>Max height</b><span>${data.max_stack_height_m.toFixed(2)} m</span></div>
      </div>
      <div class="details"><b>Pattern:</b> ${data.stowage_pattern_label}<br><b>Planning diameter:</b> ${data.planning_diameter_m.toFixed(2)} m<br><b>Status:</b> <span class="${data.status === 'OK' ? 'ok':'bad'}">${data.status}</span>
      ${data.warnings && data.warnings.length ? `<br><b>Warnings:</b><br>${data.warnings.map(w => '• ' + w).join('<br>')}` : ''}</div>
      <div class="links">
        <a href="${data.png_url}" target="_blank">PNG</a>
        <a href="${data.pdf_url}" target="_blank">PDF</a>
        <a href="${data.csv_url}" target="_blank">CSV</a>
      </div>
      <div id="allocationPanel">${allocationHtml()}</div>
    `;

    const rows = (data.block_weights || []).map(r => `
      <tr><td>${r.Block}</td><td>${Number(r.Bottom_t).toFixed(1)}</td><td>${Number(r.Wedge_t || 0).toFixed(1)}</td><td>${Number(r.Center_t || 0).toFixed(1)}</td><td>${Number(r.Upper_t || 0).toFixed(1)}</td><td><b>${Number(r.Total_t).toFixed(1)}</b></td></tr>
    `).join('');
    weightsBox.innerHTML = `
      <table>
        <thead><tr><th>Block</th><th>Bottom</th><th>Wedge</th><th>Center</th><th>Upper</th><th>Total</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
    coilDetails.innerHTML = 'Click a coil in the plan to inspect ID, weight and position.';
    drawInteractivePlan(data);
    renderAllocationSummary();

  } catch(err) {
    summaryBox.innerHTML = `<div class="details"><b>Error:</b><br>${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = 'BUILD / REFRESH PLAN';
  }
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/sw.js').catch(() => {});
}
