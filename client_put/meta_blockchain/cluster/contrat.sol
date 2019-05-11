pragma solidity ^0.4.0;
contract Ballot {

    // ENUM FOR BLOCK TYPE
    enum Block_type { Parity, Data}
 
    // STRUCT
    struct metadoc {
     
        string path;
        string creation_date;
        uint original_size;
        string blocks;
        string entangling_blocks;
    }
    struct metablock {
        string key;
        string creation_date;
        string providers;
        Block_type block_type;
        string entangled_with;
        string checksum;
        uint size;
    }
 
    // MAPPING TO STORE METADATA
    mapping (string => metablock) metablockMap;
    mapping (string => metadoc) metadocMap;
    string[] listMetablock;
    string[] listMetadoc;
  
    // METADOC
    function addMetadocMap(string path, string creationdate, string blocks, uint original_size, string entangling_blocks) public {
     
        metadocMap[path].path = path;
        metadocMap[path].creation_date = creationdate;
        metadocMap[path].original_size = original_size;
        metadocMap[path].blocks = blocks;
        metadocMap[path].entangling_blocks = entangling_blocks;
       
        listMetadoc.push(path);
    }
  
    function getMetadocMap(string path) public constant returns(string, string, uint, string) {
        return (metadocMap[path].creation_date,metadocMap[path].blocks, metadocMap[path].original_size, metadocMap[path].entangling_blocks);
    }
  
  
  
  
    // METABLOCK
    function addMetablockMap(string key, string creationdate, string providers, Block_type block_type, string checksum, uint size, string entangled_with) public {
     
        metablockMap[key].key = key;
        metablockMap[key].creation_date = creationdate;
        metablockMap[key].providers = providers;
        metablockMap[key].block_type = block_type;
        metablockMap[key].checksum = checksum;
        metablockMap[key].size = size;
        metablockMap[key].entangled_with = entangled_with;
       
        listMetablock.push(key);
    }
  
    function getMetablockMap(string key) public constant returns(string, string, Block_type, string, uint, string) {
        return (metablockMap[key].creation_date, metablockMap[key].providers, metablockMap[key].block_type, metablockMap[key].checksum, metablockMap[key].size, metablockMap[key].entangled_with);
    }
   
   
    // List of block and doc
    // block
    function getFromListMetablock(uint nb) public constant returns(string, string, string, Block_type, string, uint, string) {
       
        string key = listMetablock[nb];
        return (key, metablockMap[key].creation_date, metablockMap[key].providers, metablockMap[key].block_type, metablockMap[key].checksum, metablockMap[key].size, metablockMap[key].entangled_with);
   
    }
   
    function getNumberMetablock() public constant returns(uint) {
        return listMetablock.length;
    }
   
    // doc
    function getFromListMetadoc(uint nb) public constant returns(string, string, string, uint, string) {
       
        string path = listMetadoc[nb];
        return (path, metadocMap[path].creation_date,metadocMap[path].blocks, metadocMap[path].original_size, metadocMap[path].entangling_blocks);
    }
   
    function getNumberMetadoc() public constant returns(uint) {
       
        return listMetadoc.length;
    }
   

 
 
}

