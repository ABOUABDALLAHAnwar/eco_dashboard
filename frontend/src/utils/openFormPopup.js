export function openFormPopup(title, fields, onSubmit, initialValues={}) {
  const width=420, height=500;
  const left=window.innerWidth/2-width/2, top=window.innerHeight/2-height/2;
  const newWindow = window.open("", title, `width=${width},height=${height},top=${top},left=${left}`);
  if(!newWindow){ alert("Autorise les pop-ups !"); return; }

  newWindow.document.write(`
    <style>
      body { font-family: Arial; padding: 20px; background: #f9fafb; }
      h3 { margin-bottom: 20px; text-align: center; color: #1f2937; }
      form { display:flex; flex-direction: column; gap:12px; }
      input, select { padding:10px; border:1px solid #ccc; border-radius:6px; font-size:14px; }
      .buttons { display:flex; justify-content:flex-end; gap:10px; margin-top:20px; }
      button { padding:10px 20px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; }
      #cancelBtn { background:#e5e7eb; color:#374151; } 
      #cancelBtn:hover{background:#d1d5db;}
      button[type="submit"]{ background:#10b981; color:white; } 
      button[type="submit"]:hover{ background:#059669; }
    </style>
    <h3>${title}</h3>
    <form id="popupForm"></form>
    <div class="buttons">
      <button type="button" id="cancelBtn">Annuler</button>
      <button type="submit" form="popupForm">Envoyer</button>
    </div>
  `);

  const form = newWindow.document.getElementById("popupForm");

  fields.forEach(f => {
    if(f.type==="select"){
      const select = document.createElement("select");
      select.name = f.name;
      f.options.forEach(opt => { const option = document.createElement("option"); option.value=opt; option.innerText=opt; select.appendChild(option); });
      form.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.name=f.name; input.placeholder=f.placeholder; input.type=f.type||"text";
      input.value=initialValues[f.name]||"";
      form.appendChild(input);
    }
  });

  form.addEventListener("submit", e => { e.preventDefault();
    const values={}; fields.forEach(f=>values[f.name]=form[f.name].value);
    onSubmit(values,newWindow);
  });

  newWindow.document.getElementById("cancelBtn").addEventListener("click",()=>newWindow.close());
}
