document.getElementById("row-about").addEventListener("scroll", showAbout());


function showAbout(){
  const about = document.getElementById('row-about');
  about.style.transition = "5s";
  about.style.opacity = 1;
};
