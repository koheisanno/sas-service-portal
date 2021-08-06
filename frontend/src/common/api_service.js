import { csrftoken } from "./csrf_token.js";

async function getJSON(response) {
  if (response.status === 204) {
    return "";
  } else if (response.status === 404) {
    return null;
  } else if (!response.ok) {
    console.log(response.text())
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
