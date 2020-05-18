/**
 * confirmation de la suppression 
 * @param url 
 */
function confirm_reinit(url) {
    if (confirm("Etes-vous sûr?")) {
        window.location.href = url;
    }
}

/**
 * confirmation de la suppression 
 * @param url 
 */
function confirm_delete(url) {
    if (confirm("Etes-vous sûr?")) {
        window.location.href = url;
    }
}