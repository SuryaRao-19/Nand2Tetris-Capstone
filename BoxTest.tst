load Box.hack,
output-file BoxTest.out,
compare-to BoxTest.cmp,
output-list RAM[17728]%D2.6.2 RAM[17760]%D2.6.2 RAM[17761]%D2.6.2 RAM[17762]%D2.6.2 RAM[17763]%D2.6.2 RAM[17764]%D2.6.2 RAM[18368]%D2.6.2 RAM[18371]%D2.6.2 RAM[18400]%D2.6.2;

// 1. Untouched keyboard: box is white (0)
set RAM[24576] 0,
repeat 3000 {
  ticktock;
}
output;

// 2. Key pressed: box becomes black (-1)
set RAM[24576] 65,
repeat 3000 {
  ticktock;
}
output;

// 3. Key released: box becomes white again (0)
set RAM[24576] 0,
repeat 3000 {
  ticktock;
}
output;
