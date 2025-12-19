import { useState } from 'react';

export default function Login({onLogin}) {
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');

  const handleSubmit=(e)=>{
    e.preventDefault();
    fetch('http://localhost:8001/login',{
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body:new URLSearchParams({username:email,password})
    })
    .then(res=>res.json())
    .then(data=>onLogin(data))
    .catch(err=>alert('Erreur login'));
  }

  return (
    <div style={{display:'flex',justifyContent:'center',alignItems:'center',height:'100vh'}}>
      <form onSubmit={handleSubmit} style={{background:'white',padding:30,borderRadius:12,boxShadow:'0 6px 15px rgba(0,0,0,0.1)'}}>
        <h1>Connexion</h1>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',margin:'10px 0',padding:'10px',width:200}} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',margin:'10px 0',padding:'10px',width:200}} />
        <button type="submit" style={{padding:'10px 20px',background:'#4a6c59',color:'white',border:'none',borderRadius:6,cursor:'pointer'}}>Login</button>
      </form>
    </div>
  );
}
