(function () {
  var input = document.getElementById("idx-filter");
  if (!input) return;
  var rows = Array.prototype.slice.call(document.querySelectorAll(".idx__row"));
  var count = document.getElementById("idx-count");
  var total = rows.length;
  function run() {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (r) {
      var hit = !q || r.textContent.toLowerCase().indexOf(q) !== -1;
      r.hidden = !hit;
      if (!hit) r.open = false;
      if (hit) shown++;
    });
    if (count) count.textContent = q ? shown + " of " + total : total + " things";
  }
  input.addEventListener("input", run);
  run();
})();
