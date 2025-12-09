// Cursos disponíveis são injetados pelo template via window.fluxogramaCourses
const courseNames = Array.isArray(window.fluxogramaCourses) ? window.fluxogramaCourses : [];
const courses = courseNames.map(name => ({ name }));

const searchInput = document.getElementById("course-search");
const suggestionsContainer = document.getElementById("suggestions-container");
const feedbackEl = document.getElementById("search-feedback");
const searchTrigger = document.getElementById("course-search-trigger");

if (!searchInput || !suggestionsContainer) {
    console.warn("Fluxograma search elements not found on the page.");
} else {
    function normalizeText(text) {
        return (text || "")
            .normalize("NFD")
            .replace(/[\u0000-\u001F]/g, "")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .trim();
    }

    function clearFeedback() {
        if (feedbackEl) {
            feedbackEl.textContent = "";
            feedbackEl.classList.add("hidden");
        }
    }

    function showFeedback(message) {
        if (feedbackEl) {
            feedbackEl.textContent = message;
            feedbackEl.classList.remove("hidden");
        }
    }

    function redirectToCourse(courseName) {
        const programUrl = "/fluxograma/" + encodeURIComponent(courseName) + "/";
        window.location.href = programUrl;
    }

    function findCourseByQuery(query) {
        const normalizedQuery = normalizeText(query);
        return courses.find(course => normalizeText(course.name) === normalizedQuery);
    }

    function handleSearchSubmit() {
        const query = searchInput.value;
        const normalizedQuery = normalizeText(query);

        if (!normalizedQuery) {
            showFeedback("Digite o nome de um curso para buscar o fluxograma.");
            return;
        }

        const matchedCourse = courses.find(course => normalizeText(course.name) === normalizedQuery);
        if (matchedCourse) {
            clearFeedback();
            redirectToCourse(matchedCourse.name);
        } else {
            showFeedback("Nenhum fluxograma disponível para \"" + query.trim() + "\". Verifique o nome do curso.");
        }
    }

    searchInput.addEventListener("input", function() {
        const rawQuery = this.value;
        suggestionsContainer.innerHTML = "";

        if (!rawQuery.trim()) {
            suggestionsContainer.classList.add("hidden");
            clearFeedback();
            return;
        }

        const normalizedQuery = normalizeText(rawQuery);
        const filteredCourses = courses.filter(course =>
            normalizeText(course.name).includes(normalizedQuery)
        );

        if (filteredCourses.length > 0) {
            filteredCourses.forEach(course => {
                const suggestionItem = document.createElement("div");
                suggestionItem.classList.add("p-3", "cursor-pointer", "hover:bg-gray-100", "text-left");
                suggestionItem.textContent = course.name;
                suggestionItem.addEventListener("click", function() {
                    searchInput.value = course.name;
                    clearFeedback();
                    redirectToCourse(course.name);
                });
                suggestionsContainer.appendChild(suggestionItem);
            });
            suggestionsContainer.classList.remove("hidden");
            clearFeedback();
        } else {
            suggestionsContainer.classList.add("hidden");
            showFeedback("Nenhum fluxograma disponível para \"" + rawQuery + "\" no momento.");
        }
    });

    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSearchSubmit();
        }
    });

    if (searchTrigger) {
        searchTrigger.addEventListener("click", function(event) {
            event.preventDefault();
            handleSearchSubmit();
        });
    }

    document.addEventListener("click", function(event) {
        if (!searchInput.contains(event.target) && !suggestionsContainer.contains(event.target)) {
            suggestionsContainer.classList.add("hidden");
        }
    });
}
