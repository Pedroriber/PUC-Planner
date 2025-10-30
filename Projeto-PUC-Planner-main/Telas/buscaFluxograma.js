
const courses = [
    { name: "Engenharia da Computação", file: "fluxograma2.html" },
    { name: "Engenharia de Produção", file: "fluxograma3.html" }
];

const searchInput = document.getElementById("course-search");
const suggestionsContainer = document.getElementById("suggestions-container");

searchInput.addEventListener("input", function() {
    const query = this.value.toLowerCase();
    suggestionsContainer.innerHTML = "";

    if (query.length === 0) {
        suggestionsContainer.classList.add("hidden");
        return;
    }

    const filteredCourses = courses.filter(course => 
        course.name.toLowerCase().includes(query)
    );

    if (filteredCourses.length > 0) {
        filteredCourses.forEach(course => {
            const suggestionItem = document.createElement("div");
            suggestionItem.classList.add("p-3", "cursor-pointer", "hover:bg-gray-100", "text-left");
            suggestionItem.textContent = course.name;
            suggestionItem.addEventListener("click", function() {
                window.location.href = course.file;
            });
            suggestionsContainer.appendChild(suggestionItem);
        });
        suggestionsContainer.classList.remove("hidden");
    } else {
        suggestionsContainer.classList.add("hidden");
    }
});

document.addEventListener("click", function(event) {
    if (!searchInput.contains(event.target) && !suggestionsContainer.contains(event.target)) {
        suggestionsContainer.classList.add("hidden");
    }
});
