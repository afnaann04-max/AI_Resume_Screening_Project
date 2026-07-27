// Simple UI enhancements
document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll(".progress-bar").forEach(el=>{
    const w=el.style.width;
    el.style.width="0%";
    setTimeout(()=>el.style.width=w,300);
  });
});

function toggleDarkMode(){
 document.body.classList.toggle("bg-dark");
 document.body.classList.toggle("text-white");
}
