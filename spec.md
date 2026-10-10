# data via audio spec:
I guess this counts as amplitude key shifting.
## asyncrhonous data transfer

We will signify our data signal with a packet, defined with a couple different symbols:

## quick guide:

### frequency table:



#### data bits:
- we will have 3 symbols representing data bits in a symbol overlayed on each other. The frequency being present and not being present signals a 1 or 0.
- D0 : lsb 
- D1
- D2 : msb


#### start symbol
- signifies start of our packet 

#### end symbol
- signifies end of our packet


#### eos
- end of signal symbol we probably won't implement for now.

## ID Tagging:
An important feature to distuingish from hearing your own packets is ID Tagging, 
we can tag all 3 symbols with a unique frequency which will be used as an ID.