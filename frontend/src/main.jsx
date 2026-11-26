import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import './style.css';

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const TABS = ['Overview','Colony Explorer','Forecast','Climate Factors','Spatial Map','Graph View','XAI','Risk Dashboard','Data Quality','Validation','Lineage','Live Sensor'];

async function api(path, options={}) {
  const res = await fetch(`${API}${path}`, options);
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

function Card({label, value, hint}) { return <div className="card"><span>{label}</span><strong>{value}</strong>{hint && <small>{hint}</small>}</div> }
function Panel({title, children, right}) { return <section className="panel"><div className="panel-title"><h2>{title}</h2>{right}</div>{children}</section> }
function Badge({children, tone=''}) { return <span className={`badge ${tone}`}>{children}</span> }

function App(){
  const [tab,setTab]=useState('Overview');
  const [colonies,setColonies]=useState([]);
  const [forecasts,setForecasts]=useState([]);
  const [metrics,setMetrics]=useState({});
  const [validation,setValidation]=useState(null);
  const [lineage,setLineage]=useState(null);
  const [explanations,setExplanations]=useState([]);
  const [selected,setSelected]=useState('');
  const [colony,setColony]=useState(null);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);
  const [sensor,setSensor]=useState({temperature:-8.4,seaIce:0.74,ocean:-0.31,updated:'—'});

  const refresh = async () => {
    setLoading(true); setError('');
    try {
      const [c,f,m,v,e,l] = await Promise.all([
        api('/api/colonies'), api('/api/forecast'), api('/api/metrics'),
        api('/api/validation'), api('/api/explanations/COLONY_001'), api('/api/lineage/demo')
      ]);
      setColonies(c); setForecasts(Array.isArray(f)?f:[]); setMetrics(m||{}); setValidation(v); setExplanations(e?.factors||[]); setLineage(l);
      if (!selected && c.length) setSelected(c[0].colony_id);
    } catch (err) { setError(`Backend connection failed. Start the demo with ./run_demo.sh. ${err.message}`); }
    finally { setLoading(false); }
  };
  useEffect(()=>{refresh()},[]);
  useEffect(()=>{ if(!selected) return; api(`/api/colonies/${selected}`).then(setColony).catch(e=>setError(e.message)); },[selected]);

  const forecast = useMemo(()=>forecasts.find(x=>x.colony_id===selected),[forecasts,selected]);
  const history = useMemo(()=> (colony?.history||[]).map(x=>({...x,date:x.survey_date,population:x.population_count})),[colony]);
  const climate = useMemo(()=> (colony?.history||[]).map(x=>({date:x.survey_date,SST:x.sea_surface_temperature,SeaIce:x.sea_ice_concentration,AirTemp:x.air_temperature,Chlorophyll:x.chlorophyll_concentration})),[colony]);
  const riskCounts = useMemo(()=>['LOW','MEDIUM','HIGH'].map(r=>({risk:r,count:forecasts.filter(x=>x.risk_level===r).length})),[forecasts]);
  const graphEdges = useMemo(()=>{
    const edges=[]; for(let i=0;i<colonies.length;i++) for(let j=i+1;j<colonies.length;j++){
      const a=colonies[i],b=colonies[j]; const d=Math.hypot((a.latitude-b.latitude), (a.longitude-b.longitude));
      if(d<8) edges.push({a:a.colony_id,b:b.colony_id,distance:d.toFixed(2)});
    } return edges;
  },[colonies]);
  const quality = validation?.quality || validation?.data_quality || {};

  const forecastSeries = history.length ? [...history,{date:'Next survey',population:forecast?.forecast,lower:forecast?.lower_bound,upper:forecast?.upper_bound}] : [];

  return <div className="app">
    <header className="hero">
      <div><div className="eyebrow">CLIMATE-15 </div><h1>Antarctic Penguin Forecasting</h1><p>Climate-Aware Spatio-Temporal Graph Neural Network</p></div>
      <div className="status"><span className="dot"></span>{loading?'Connecting…':'System online'}<button onClick={refresh}>Refresh</button></div>
    </header>
    <nav>{TABS.map(x=><button key={x} className={tab===x?'active':''} onClick={()=>setTab(x)}>{x}</button>)}</nav>
    {error && <div className="error"><b>API error:</b> {error}</div>}
    <main>
      {tab==='Overview' && <>
        <div className="cards">
          <Card label="Total colonies" value={colonies.length} hint="Fixture observations"/>
          <Card label="Forecasts" value={forecasts.length} hint="Latest model run"/>
          <Card label="Lineage coverage" value={`${metrics.lineage_coverage ?? 0}%`} hint="Traceable outputs"/>
          <Card label="Data rows" value={metrics.data_validation?.rows ?? '—'} hint={metrics.data_validation?.valid?'Schema valid':'Validation required'}/>
        </div>
        <Panel title="Forecast snapshot" right={<Badge tone="info">ST-GNN v1.0.0</Badge>}>
          <div className="table-wrap"><table><thead><tr><th>Colony</th><th>Species</th><th>Forecast</th><th>95% interval</th><th>Confidence</th><th>Risk</th></tr></thead><tbody>{forecasts.map(f=>{const c=colonies.find(x=>x.colony_id===f.colony_id);return <tr key={f.colony_id} onClick={()=>{setSelected(f.colony_id);setTab('Colony Explorer')}}><td>{f.colony_id}</td><td>{c?.species||'—'}</td><td>{f.forecast?.toFixed(1)}</td><td>{f.lower_bound?.toFixed(1)} – {f.upper_bound?.toFixed(1)}</td><td>{(f.confidence*100).toFixed(1)}%</td><td><Badge tone={f.risk_level.toLowerCase()}>{f.risk_level}</Badge></td></tr>})}</tbody></table></div>
        </Panel>
        <div className="grid2"><Panel title="Risk distribution"><ResponsiveContainer width="100%" height={250}><BarChart data={riskCounts}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="risk"/><YAxis allowDecimals={false}/><Tooltip/><Bar dataKey="count"/></BarChart></ResponsiveContainer></Panel><Panel title="Validation & governance"><div className="governance"><div><b>Source</b><span>{lineage?.source||'—'}</span></div><div><b>Dataset</b><span>{lineage?.dataset_version||'—'}</span></div><div><b>Model</b><span>{lineage?.model_version||'—'}</span></div><div><b>Prediction</b><span>{lineage?.prediction_version||'—'}</span></div></div></Panel></div>
      </>}

      {tab==='Colony Explorer' && <Panel title="Colony Explorer" right={<select value={selected} onChange={e=>setSelected(e.target.value)}>{colonies.map(c=><option key={c.colony_id} value={c.colony_id}>{c.colony_id} — {c.species}</option>)}</select>}>
        {colony && <><div className="stats"><div><b>{colony.species}</b><span>Species</span></div><div><b>{colony.latitude}, {colony.longitude}</b><span>Coordinates</span></div><div><b>{history.length}</b><span>Observations</span></div><div><b>{forecast?.risk_level||'—'}</b><span>Risk</span></div></div><ResponsiveContainer width="100%" height={360}><LineChart data={history}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="date"/><YAxis/><Tooltip/><Legend/><Line type="monotone" dataKey="population" name="Observed population" strokeWidth={3}/></LineChart></ResponsiveContainer></>}
      </Panel>}

      {tab==='Forecast' && <Panel title="Forecast with uncertainty" right={<select value={selected} onChange={e=>setSelected(e.target.value)}>{colonies.map(c=><option key={c.colony_id} value={c.colony_id}>{c.colony_id}</option>)}</select>}>
        {forecast && <><div className="forecast-banner"><div><span>Point forecast</span><strong>{forecast.forecast.toFixed(1)}</strong></div><div><span>Lower bound</span><strong>{forecast.lower_bound.toFixed(1)}</strong></div><div><span>Upper bound</span><strong>{forecast.upper_bound.toFixed(1)}</strong></div><div><span>Confidence</span><strong>{(forecast.confidence*100).toFixed(2)}%</strong></div></div><ResponsiveContainer width="100%" height={380}><AreaChart data={forecastSeries}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="date"/><YAxis/><Tooltip/><Legend/><Area type="monotone" dataKey="upper" stackId="1" stroke="none" fill="transparent"/><Area type="monotone" dataKey="lower" stackId="1" stroke="none" fill="transparent"/><Line type="monotone" dataKey="population" name="Observed" strokeWidth={3}/><Line type="monotone" dataKey="lower" name="Lower" strokeDasharray="5 5"/><Line type="monotone" dataKey="upper" name="Upper" strokeDasharray="5 5"/></AreaChart></ResponsiveContainer><p className="note">Interval width is derived from calibrated residual uncertainty and data-quality/sparsity factors; it is not a manually assigned confidence value.</p></>}
      </Panel>}

      {tab==='Climate Factors' && <Panel title={`Climate history — ${selected}`}><ResponsiveContainer width="100%" height={400}><LineChart data={climate}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="date"/><YAxis/><Tooltip/><Legend/><Line dataKey="SST" name="Sea surface temp"/><Line dataKey="SeaIce" name="Sea ice concentration"/><Line dataKey="AirTemp" name="Air temperature"/><Line dataKey="Chlorophyll" name="Chlorophyll"/></LineChart></ResponsiveContainer></Panel>}

      {tab==='Spatial Map' && <Panel title="Spatial colony map"><div className="map"><div className="map-grid"></div>{colonies.map(c=>{const left=((c.longitude+70)/20)*100;const top=((c.latitude+75)/15)*100;return <button key={c.colony_id} className="map-node" style={{left:`${Math.max(4,Math.min(96,left))}%`,top:`${Math.max(6,Math.min(94,top))}%`}} onClick={()=>{setSelected(c.colony_id);setTab('Colony Explorer')}} title={`${c.colony_id} · ${c.species}`}>●<span>{c.colony_id.replace('COLONY_','')}</span></button>})}<div className="map-label">Antarctic colony locations · schematic lat/lon projection</div></div></Panel>}

      {tab==='Graph View' && <Panel title="Spatial graph"><div className="graph"><svg viewBox="0 0 800 420">{graphEdges.map((e,i)=>{const a=colonies.find(c=>c.colony_id===e.a),b=colonies.find(c=>c.colony_id===e.b);const ax=((a.longitude+70)/20)*760+20, ay=((a.latitude+75)/15)*380+20,bx=((b.longitude+70)/20)*760+20,by=((b.latitude+75)/15)*380+20;return <line key={i} x1={ax} y1={ay} x2={bx} y2={by} strokeWidth="2"/>})}{colonies.map(c=>{const x=((c.longitude+70)/20)*760+20,y=((c.latitude+75)/15)*380+20;return <g key={c.colony_id}><circle cx={x} cy={y} r="16"/><text x={x} y={y-24} textAnchor="middle">{c.colony_id.replace('COLONY_','')}</text></g>})}</svg></div><p className="note">Edges are derived from geographic proximity for visualization. The model configuration uses k-nearest spatial message passing.</p></Panel>}

      {tab==='XAI' && <Panel title="Explainability"><div className="xai-list">{explanations.map((x,i)=><div className="xai-row" key={x.factor}><span>{i+1}. {x.factor}</span><div className="bar"><i style={{width:`${Math.min(100,Math.max(0,x.importance))}%`}}></i></div><b>{x.importance.toFixed(2)}</b></div>)}</div><p className="note">Method reported by the backend: model-derived feature ablation. Values are retrieved from the generated explanation artifact rather than invented by the UI.</p></Panel>}

      {tab==='Risk Dashboard' && <Panel title="Risk classification"><div className="risk-grid">{forecasts.map(f=><div className={`risk-card ${f.risk_level.toLowerCase()}`} key={f.colony_id}><h3>{f.colony_id}</h3><Badge tone={f.risk_level.toLowerCase()}>{f.risk_level}</Badge><p>Forecast: <b>{f.forecast.toFixed(1)}</b></p><p>Observations: {f.n_observations}</p><p>Survey quality: {f.survey_quality}</p><p>Time gap: {f.time_delta_days} days</p></div>)}</div><p className="note">Risk is displayed from the model artifact. Sparse evidence and wider uncertainty are treated as degraded-risk conditions.</p></Panel>}

      {tab==='Data Quality' && <><Panel title="Data quality"><div className="quality-grid"><Card label="Rows" value={metrics.data_validation?.rows??0}/><Card label="Schema" value={metrics.data_validation?.valid?'VALID':'INVALID'}/><Card label="Missingness" value={quality.missing_values??'—'}/><Card label="Sparse colonies" value={quality.sparse_colonies??'—'}/></div><pre>{JSON.stringify(validation,null,2)}</pre></Panel></>}

      {tab==='Validation' && <Panel title="Validation & acceptance evidence"><div className="cards"><Card label="MAE" value={metrics.mae??'—'}/><Card label="RMSE" value={metrics.rmse??'—'}/><Card label="Interval coverage" value={metrics.interval_coverage?`${metrics.interval_coverage}%`:'—'}/><Card label="Lineage" value={`${metrics.lineage_coverage??0}%`}/></div><pre>{JSON.stringify(metrics,null,2)}</pre></Panel>}

      {tab==='Lineage' && <Panel title="Prediction lineage"><div className="lineage"><div><b>Source</b><span>{lineage?.source}</span></div><div><b>Source URL</b><span>{lineage?.source_url}</span></div><div><b>Dataset version</b><span>{lineage?.dataset_version}</span></div><div><b>File hash</b><span className="mono">{lineage?.file_hash}</span></div><div><b>Transformation</b><span>{lineage?.transformation}</span></div><div><b>Model version</b><span>{lineage?.model_version}</span></div><div><b>Prediction version</b><span>{lineage?.prediction_version}</span></div><div><b>Git commit</b><span>{lineage?.git_commit}</span></div></div></Panel>}

      {tab==='Live Sensor' && <Panel title="Live environmental sensor simulation" right={<button className="primary" onClick={()=>setSensor({temperature:+(-10+Math.random()*5).toFixed(2),seaIce:+(0.55+Math.random()*0.35).toFixed(3),ocean:+(-0.7+Math.random()*0.8).toFixed(3),updated:new Date().toLocaleTimeString()})}>Generate reading</button>}><div className="sensor-grid"><Card label="Air temperature" value={`${sensor.temperature} °C`} hint={sensor.updated}/><Card label="Sea ice" value={sensor.seaIce} hint="fraction"/><Card label="Ocean condition" value={sensor.ocean} hint="simulated index"/></div><div className="sensor-flow"><span>Sensor</span><b>→</b><span>JSON / serial</span><b>→</b><span>Validation</span><b>→</b><span>FastAPI</span><b>→</b><span>Forecast pipeline</span></div><p className="note">This is an optional software sensor interface for the Review 2 hardware-interfacing component; the capstone remains runnable without physical hardware.</p></Panel>}
    </main>
    <footer>Offline demo data is synthetic and explicitly labelled. Backend: {API}</footer>
  </div>
}

createRoot(document.getElementById('root')).render(<App/>);
