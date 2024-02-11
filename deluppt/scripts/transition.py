from deluppt.scripts.objects.dummy import dummy

from pprint import pprint

class transition:
    
    ignore_args = ['pos', 'size', 'styles', 'animations']
    all_tags = []
    obj2id = {}
    
    def similar_object_search(
            notags1:list[dummy],
            notags2:list[dummy]
        ) -> tuple[ list[ tuple[ dummy, dummy ] ], tuple[ list[ dummy ], list[ dummy ]] ]:
        '''
        return couple, (remained1, remained2)
        '''
        
        count = min(len(notags1), len(notags2))
        i :int
        remained1 :list
        remained2 :list
        used_obj :list = []
        
        notags1 = sorted(notags1, key=lambda x:transition.obj2id[x])
        notags2 = sorted(notags2, key=lambda x:transition.obj2id[x])
        couple = []
        
        for object1 in notags1:
            i = 0
            # print("="*30)
            # print(f"{object1=}")
            while (i < count):
                object2 = notags2[i]
                i += 1
                
                # print(f"{object2=}")
                if (type(object1) != type(object2)): continue
                count -= 1
                notags2.remove(object2)
                couple.append((object1, object2))
                used_obj += [object1, object2]
                break
        
        remained1 = [obj for obj in notags1 if obj not in used_obj]
        remained2 = [obj for obj in notags2 if obj not in used_obj]
        
        return couple, (remained1, remained2)
    
    def tag_search(
            tags1:dict[ str : dummy ],
            tags2:dict[ str : dummy ]
        ) -> tuple[ list[ tuple[ dummy, dummy ] ], tuple[ list[ dummy ], list[ dummy ] ] ]:
        
        couple = []
        used_tags = []
        reamined1 = []
        reamined2 :list
        
        for t1 in tags1:
            
            if (t1 not in tags2):
                reamined1.append(tags1[t1])
                continue
            
            used_tags.append(t1)
            couple.append((tags1[t1], tags2[t1]))
            
            continue
        
        reamined2 = [tags2[t] for t in tags2 if t not in used_tags]
        
        return couple, (reamined1, reamined2)
    
    def distinguish(objects:list[dummy]) -> tuple[ dict, list ]:
        '''
        if same tag exist -> top layer maintain it's tag, else lose their tags
        '''
        
        tags :dict = {}
        notags :list = []
        
        for i, object in enumerate(reversed(objects)):
            transition.obj2id[object] = i
            tag :str = object.tag
            if (tag):
                if (tag in tags): notags.append(object)
                else: tags[tag] = object
            else: notags.append(object)
            
            continue
        
        transition.all_tags += [t for t in list(tags.keys()) if t not in transition.all_tags]
        
        return tags, notags
    
    def sort_similar_objects(objects1:list[dummy], objects2:list[dummy], sortby:bool=0) -> dict[dummy:int]:
        '''
        tag search -> similar search (must match: type) (except: pos, size, styles, animations)
        '''
        
        # reset
        transition.all_tags = []
        
        # define
        tags1 :dict # tags : object
        tags2 :dict # tags : object
        notags1 :list
        notags2 :list
        
        tagged :list
        couple :list
        remained1 :list
        remained2 :list
        decoded :dict = {}
        
        # distinguish
        tags1, notags1 = transition.distinguish(objects1)
        tags2, notags2 = transition.distinguish(objects2)
        
        # tag search
        tagged, (remained1, remained2) = transition.tag_search(tags1, tags2)
        
        # add remained to notags
        notags1 += remained1
        notags2 += remained2
        
        # similar search
        couple, (remained1, remained2) =transition.similar_object_search(notags1, notags2)
        
        # update
        tagged += couple
        
        # sort
        tagged += remained1
        tagged += remained2
        tagged = sorted(tagged, key=lambda x:transition.obj2id[x[sortby] if type(x) == tuple else transition.obj2id.get(x, len(transition.obj2id))], reverse=True)

        
        for objects in tagged:
            if (type(objects) == tuple):
                decoded[objects] = (0, 1)
            else:
                if (objects in objects1): decoded[objects] = 0
                else: decoded[objects] = 1
        
        return decoded