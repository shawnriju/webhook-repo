function formatTimestamp(isoString) {
  const date = new Date(isoString);

  const day = date.getUTCDate();
  const month = date.toLocaleString("en-GB", { month: "long", timeZone: "UTC" });
  const year = date.getUTCFullYear();

  let hours = date.getUTCHours();
  const minutes = date.getUTCMinutes().toString().padStart(2, "0");
  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12;

  const suffix =
    day % 10 === 1 && day !== 11 ? "st" :
    day % 10 === 2 && day !== 12 ? "nd" :
    day % 10 === 3 && day !== 13 ? "rd" : "th";

  return `${day}${suffix} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
}


async function fetchEvents() {
  const res = await fetch("/webhook/events");
  const events = await res.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  events.forEach(e => {
    let text = "";
    const time = formatTimestamp(e.timestamp);

    if (e.action === "push") {
      text = `"${e.author}" pushed to "${e.to_branch}" on ${time}`;
    }

    if (e.action === "pull_request") {
      text = `"${e.author}" submitted a pull request from "${e.from_branch}" to "${e.to_branch}" on ${time}`;
    }

    if (e.action === "merge") {
      text = `"${e.author}" merged branch "${e.from_branch}" to "${e.to_branch}" on ${time}`;
    }

    const li = document.createElement("li");
    li.innerText = text;
    list.appendChild(li);
  });
}

setInterval(fetchEvents, 15000);
fetchEvents();
