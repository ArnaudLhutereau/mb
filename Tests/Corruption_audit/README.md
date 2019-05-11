# Corruption audit

This script is used to compare and detect corrupted, missing or unexpected entries in Redis database which store metadata files.
In case of problem with one or more entries, the script will be in charge to add the entry name to a message queue, which
will be read by the rebuilding script in the background.

### Design

``` bash
# System initialisation
Redis()
Blockchain()
MessageQueue()

# Variables
nb_blockchain_entry = Blockchain.getNumberEntry()
list_entries_redis = Redis.getListEntries()
counter = 0

while(counter < nb_blockchain_entry):
	metadata_blockchain = Blockchain.getNumber(counter)
	metadata_redis = Redis.read(metadata_blockchain)
	if(metadata_blockchain != metadata_redis):
		MessageQueue.append(metadata_blockchain)
	else:
		Redis.addField(metadata_redis, "audit")
	counter++
	
for entry in list_entries_redis:
	if(Redis.field_exists(entry, "audit"):
		Redis.field_delete(entry, "audit)
	else:
		Redis.delete(entry)

```

During the first loop, the script compare all fields of metadata. We separates metadata in two types with their sorted fields :

* metablock (key, creation_date, providers, block_type, checksum, size)
* metadoc (path, creation_date, list_of_blocks, original_size, entangling_blocks)

At the line of comparison "if(metadata_blockchain != metadata_redis)", we compare all metablock but in the real script
it's a little bit more complicated because first, we check the key, then the date of creation...

We do the same with metadoc: path in first, then date of creation..

That's why there is a difference of running time that you can see in the results part, between an audit without error and
an audit with the worst situation : problem inside the last field of a metablock (size) and a metadoc (entangling_blocks).


### How to use it:

#### Parameters
At the beginning of the file, you can change the name of the audit to be sure that a potential hacker can't guess the audit
number to falsify the audit.

#### Command line
You have to be in the client_rebuild container which owns the script to launch the audit.
``` bash
cd /home/meta_blockchain/
python3 check_corruption.py
```

#### How to corrupt files?

To be in the worst possible situation, in according to the design of the script, we used a script called "delete_one_field.py".

The goal is to delete one field for each entry in Redis. And the deleted field is the worst for the audit comparison phase,
because the deleted field is the last field which is compared for each entry.

By default all metablock will have the "size" field deleted, and for all metadoc it's the "entangling_blocks" field.

You can launch it with, when you are in the "client_rebuild" container with:
``` bash
cd /home/meta_blockchain/
python3 delete_one_field.py
```

### Results
All results is composed by the time to compare entries and the time to rebuild if it needs

#### First test : 100 files
For the first test, the audit script has verified 100 files (it's mean 400 entries)

```
Without error: 2.6557 seconds
With the worst error : 3.7170 seconds
```

#### Second test : 1000 files
For the second test, the audit script has verified 1000 files (it's mean 4000 entries)
```
Without error: 26,42 seconds
With the worst error : 37 seconds
```
