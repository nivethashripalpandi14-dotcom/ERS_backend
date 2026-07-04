const loadBtn = document.getElementById("loadBtn");
const postsContainer = document.getElementById("posts");
const postBtn = document.getElementById("postBtn");

const deleteBtn = document.getElementById("deleteBtn");
const putBtn = document.getElementById("putBtn");



loadBtn.addEventListener("click", async () => {
    postsContainer.innerHTML = "Loading...";

    try {
        const response = await fetch(
            "http://192.168.2.5:8000/users/"
        );

        const posts = await response.json();
        // console.log(data);
        console.log("Response", response)
        console.log("post", posts)
        postsContainer.innerHTML = "";
        // postsContainer.innerHTML = data;

        posts.forEach(post => {
            const postDiv = document.createElement("div");
            postDiv.classList.add("post");

            postDiv.innerHTML = `
                <h6>${post.title}</h6>
                <p>${post.body}</p>
                <p>${post.userId}</p>

            `;

            postsContainer.appendChild(postDiv);
        });

    } catch (error) {
        postsContainer.innerHTML = "Failed to load data.";
        console.error(error);
    }
});


const result = document.getElementById("result");

// POST
postBtn.addEventListener("click", async () => {
    postsContainer.innerHTML = "Loading...";
    try {
        const response = await fetch(
            "http://192.168.2.5:8000/users/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: "sagar",
                    email: "sagar@gmail.com",
                    phone_number: "1234567890"
                })
            }
        );

        const data = await response.json();
        console.log("post", data)

        result.textContent =
            "POST Success:\n\n" +
            JSON.stringify(data, null, 2);

    } catch (error) {
        console.error(error);
    }
}
)

// PUT
putBtn.addEventListener("click", async () => {
    try {
        const response = await fetch(
            "http://192.168.2.5:8000/users/4",
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username:"nivetha"
                })
            }
        );
        const data = await response.json();
        console.log("put", data)


        result.textContent =
            "PUT Success:\n\n" +
            JSON.stringify(data, null, 2);

    } catch (error) {
        console.error(error);
    }
}
)
// DELETE

deleteBtn.addEventListener("click", async () => {
    postsContainer.innerHTML = "Loading...";
    try {
        const response = await fetch(
            "http://192.168.2.5:8000/users/6",
            {
                method: "DELETE"
            }
        );

        result.textContent =
            `DELETE Success\n\nStatus: ${response.status}`;

    } catch (error) {
        console.error(error);
    }
}
)