
var load_card = function(){

    cards.push(["Apple Card", "Apple Card offers up to 3% Daily Cash back on purchases with no fees. Apply with no impact to your credit score to see if you're approved. Terms apply. "]);
    cards.push(["Citibank credit card", "Citibank credit card offers 2% cashback on all purchases and partners with Walmart, providing a 10% discount on food purchases."]);
    cards.push(["Chase Card", "The Chase Card offers a 5% discount at BestBuy, with a maximum discount of $100."]);
}

var get_card_prompt = function(){
    const combinedString = cards.map(card => `${card[0]}: ${card[1]}`).join('\n\n');

    return combinedString;
}

var get_card_list = function(){
    const combinedString = cards.map(card => `${card[0]}`).join(',');
    return combinedString;
}