Produce an array of URLs using https://arcraiders.wiki/wiki/Ammo

```
var ammoTypes = [...document.querySelectorAll("table tr")]
  .map(row => row.querySelector("td:first-child a, th:first-child a"))
  .filter(a => a)
  .map(a => a.text);

console.log(ammoTypes);
```
