Produce an array of URLs using https://arcraiders.wiki/wiki/Loot

```
const firstColumnHrefs = [...document.querySelectorAll("table tr")]
  .map(row => row.querySelector("td:first-child a, th:first-child a"))
  .filter(a => a)   // only keep rows that contain an <a>
  .map(a => a.href);

console.log(firstColumnHrefs);
```
