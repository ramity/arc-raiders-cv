Produce an array of URLs using https://arcraiders.wiki/wiki/Loot

```
var lootIconURLs = [...document.querySelectorAll("table tr")]
  .map(row => row.querySelector("td:first-child a, th:first-child a"))
  .filter(a => a)
  .map(a => a.href);

console.log(lootIconURLs);
```
