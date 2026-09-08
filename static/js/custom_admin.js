// Zar belle CRM - Chiroyli va qulay Saqlash tugmasi hamda Ctrl+S qo'llab-quvvatlashi

document.addEventListener("DOMContentLoaded", function () {
    const changelistForm = document.getElementById("changelist-form");
    if (!changelistForm) return;

    // Asl pastki saqlash tugmasini topamiz
    const originalSaveBtn = changelistForm.querySelector('input[type="submit"][name="_save"]') ||
                            changelistForm.querySelector('button[type="submit"][name="_save"]') ||
                            changelistForm.querySelector('.card-footer input[type="submit"]');

    if (!originalSaveBtn) return;

    // 1. Yuqoriga (Top Toolbar) nusxalangan "Saqlash" tugmasini qo'shish
    const actionsContainer = document.querySelector(".actions") || document.querySelector("#changelist-search");
    if (actionsContainer) {
        const topSaveBtn = document.createElement("button");
        topSaveBtn.type = "button";
        topSaveBtn.className = "btn btn-success top-save-button ml-2";
        topSaveBtn.innerHTML = '<i class="fas fa-save mr-1"></i> Saqlash (Ctrl+S)';
        topSaveBtn.title = "O'zgarishlarni saqlash uchun bosing yoki Ctrl+S tugmasini bosing";
        
        topSaveBtn.addEventListener("click", function () {
            originalSaveBtn.click();
        });

        actionsContainer.appendChild(topSaveBtn);
    }

    // 2. Doim ko'rinib turuvchi Floating (Yopishqoq) Saqlash tugmasi
    const floatingBtn = document.createElement("button");
    floatingBtn.type = "button";
    floatingBtn.id = "floating-save-btn";
    floatingBtn.className = "floating-save-btn btn btn-primary shadow-lg";
    floatingBtn.innerHTML = '<i class="fas fa-save mr-2"></i> Saqlash <span class="badge badge-light ml-1" id="change-counter" style="display:none;">0</span>';
    floatingBtn.title = "O'zgarishlarni saqlash (Ctrl+S)";
    
    floatingBtn.addEventListener("click", function () {
        originalSaveBtn.click();
    });

    document.body.appendChild(floatingBtn);

    // 3. Jadvaldagi checkbox yoki inputlar o'zgarganda floating tugmani ajratib ko'rsatish
    let modifiedCount = 0;
    const editableInputs = changelistForm.querySelectorAll("table input, table select");
    const changeCounter = document.getElementById("change-counter");

    editableInputs.forEach(input => {
        input.addEventListener("change", function () {
            modifiedCount++;
            floatingBtn.classList.add("btn-success");
            floatingBtn.classList.remove("btn-primary");
            if (changeCounter) {
                changeCounter.innerText = modifiedCount;
                changeCounter.style.display = "inline-block";
            }
        });
    });

    // 4. Ctrl+S yoki Cmd+S bosilganda avtomatik saqlash
    document.addEventListener("keydown", function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === "s") {
            e.preventDefault();
            originalSaveBtn.click();
        }
    });
});
