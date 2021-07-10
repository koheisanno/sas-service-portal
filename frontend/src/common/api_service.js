import { csrftoken } from "./csrf_token.js";

async function getJSON(response) {
  console.log(response.status);
  if (response.status === 404) {
    return null;
  } else if (!response.ok) {
    console.log(response.text())
    return false;
  } else {
    return response.json();
  }
}

function apiService(endpoint, method, data) {
  const config = {
    method: method || "GET",
    body: data !== undefined ? JSON.stringify(data) : null,
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  };

  return fetch(endpoint, config)
    .then(getJSON)
    .catch((error) => console.log(error));
}

function apiImageService(endpoint, method, data) {
  const config = {
    method: method || "GET",
    body: data !== undefined ? data : null,
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };

  return fetch(endpoint, config)
    .then(getJSON)
    .catch((error) => console.log(error));
}

export { apiService,  apiImageService};
