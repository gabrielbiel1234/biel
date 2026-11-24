const $ = s => document.querySelector(s);
document.querySelectorAll(".nav").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".nav").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(x=>x.classList.remove("visible"));
  btn.classList.add("active"); $("#"+btn.dataset.tab).classList.add("visible");
}));
function bubble(text, who){const el=document.createElement("div");el.className="bubble "+who;el.textContent=text;$("#messages").appendChild(el);$("#messages").scrollTop=$("#messages").scrollHeight;return el;}
$("#chatForm").addEventListener("submit", async e=>{
  e.preventDefault();const message=$("#message").value.trim();if(!message)return;
  bubble(message,"user");$("#message").value="";const waiting=bubble("Pensando...","bot");
  try{const r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message})});const data=await r.json();waiting.textContent=data.reply||data.error||"Sem resposta.";}
  catch(err){waiting.textContent="Não consegui conectar ao servidor ULTRA AI. Confira se start.bat está aberto.";}
});
$("#createBtn").addEventListener("click",async()=>{
  const description=$("#description").value.trim();if(!description){$("#buildStatus").textContent="Descreva o aplicativo primeiro.";return;}
  $("#createBtn").disabled=true;$("#buildStatus").textContent="A IA está criando seu aplicativo. Isso pode levar alguns minutos...";
  $("#result").classList.remove("show");
  try{
    const r=await fetch("/api/create-app",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({description})});
    const data=await r.json();
    if(!r.ok)throw new Error(data.error||"Falha ao criar.");
    $("#buildStatus").textContent="Aplicativo criado com sucesso!";
    $("#result").innerHTML="";
    const title=document.createElement("b");title.textContent="Arquivos gerados: "+data.files.join(", ");
    const p=document.createElement("p");p.textContent="Pasta: "+data.path;
    const a=document.createElement("a");a.href=data.preview;a.target="_blank";a.rel="noopener";a.textContent="Abrir prévia do aplicativo ↗";
    $("#result").append(title,p,a);$("#result").classList.add("show");
  }catch(err){$("#buildStatus").textContent=err.message;}
  finally{$("#createBtn").disabled=false;}
});
