
var load_shopping = function(){
    shoppingList.push(["Pixel8 Phone", 599]);
    shoppingList.push(["Chromebook", 1099]);
    shoppingList.push(["BigScreen TV", 899]);
    shoppingList.push(["Beef Stack", 59]);
    shoppingList.push(["Coke-Cola family size", 30]);
    shoppingList.push(["Chocolate Cake", 29]);
    shoppingList.push(["A black men's suit", 199]);
    shoppingList.push(["Dehumidifier", 399]);
    shoppingList.push(["Bladeless fan", 499]);
}

// 獲取選中的商品
function getSelectedProducts() {
    const selectedProducts = [];
    const selectedElements = shoppingListElement.getElementsByClassName("selected");
    for (let i = 0; i < selectedElements.length; i++) {
        const index = Array.from(shoppingListElement.children).indexOf(selectedElements[i]);
        selectedProducts.push(shoppingList[index]);
    }
    console.log("Selected Products: " + JSON.stringify(selectedProducts));
    return selectedProducts;
}

var get_shopping_prompt = function(){
    var cart = getSelectedProducts();
    var output = cart.map(cart => `${cart[0]}: ${cart[1]}`).join('\n');

    return  "My shopping list:\n" + output + "\n";
}