# 크래프톤 정글 4기 Red-Black Tree 후기, 정리, 팁

차후 C언어로 진행하는 프로젝트 (malloc, PintOS, etc.)를 위해 C언어와 친근해지는 과제 (근대 Red-Black Tree는 너무햇...). 

Tree 자료구조가 높이 조절을 따로 안하면 최악의 경우 배열과 다름없는 구조가 되어버려서 높이를 log(n)을 유지하기 위해 Balance Tree를 유지하기 위한 추가적이 제약조건이 붙어서 사용된다. 대표적인 Balanced Tree는 B-Tree, AVL Tree, RB Tree가 있다.

- ***B-Tree***는 삽입/삭제 전에 미리 밑작업을 진행하여 삽입/삭제되는 순간 균형이 잡혀있어 따로 추가적인 작업은 안해도된다. (대신 밑작업이 복잡하다)
- ***AVL Tree***는 삽입/삭제 후 rotation을 활용하여 균형을 잡는다. 균형을 잡기 위해 높이를 따로 노드에 저장해야하며 int 타입으로 인해 총 4 바이트를 먹게된다. 추가적으로 RB Tree보다 더 강한 제약조건을 유지해야해서 삽입/삭제 한번에 rotation을 많이 쓰게 되는 경우도 있다. 대신 탐색이 RB Tree 보다 빠르다.
- ***RB Tree***는 삽입/삭제 후 rotation을 활용하여 균형을 잡는다. 균형을 잡기 위해 노드에게 색을 부여하며 char 타입으로 충분이 커버가능해서 1 바이트를 먹게된다. 균형을 잡기위한 제약조건으로 인해 삽입/삭제 최악의 경우 double rotation을 사용한다. 대체적으로 Balanced Tree를 사용해야하는 상황이면 RB Tree를 사용한다.

정글에게 주어진 RB Tree 이론/논리 이해 + 구현 시간 + 기본적인 CS 지식으로는 사실상 제로베이스에서 빌드업하기는 매우 어렵다 (만약 제로베이스에서 가능하시다면... ~~돔황챠!~~). CLRS (알고리즘 책)에서 의사코드로 깔끔하게 정리 되있어서, 이론/논리 이해 후 의사코드의 뼈대와 추가적인 인터넷에서 C코드 구현하는 부분들을 찾아보면서 과제를 진행했다. 개인적으로 C에서 Segmentation Fault 오류로 인해 디버깅이 어려워서 RBTree Insert/Erase는 Python으로 먼저 전부다 구현 완성하고 C로 했다.

## 주어진 Function 외 추가적으로 구현한 Functions
- `rotate_left(rbtree, node)` + `rotate_right(rbtree, node)`: 이걸 생각해내고 구현한 사람은 미친놈이다. 이게 Balance Tree의 심장이라고 생각한다.
- `insert_fix(rbtree, node)` : 삽입 후 제약조건에 어긋나는 상황이 발생시 활용.
- `transplant(rbtree, node_delete, node_substitute)`: 삭제발생시 삭제하는 노드가 단말 노드가 아닐시 활용.
- `*subtree_find_min(rbtree, node)`: 대체할 노드 찾아주는 함수.
- `erase_fix(rbtree, node)`: 삭제 후 제약조건에 어긋나는 상황이 발생시 활용.
- `inorder_trav(rbtree, *array, tree_size, *node, *count)`: 테스트 케이스가 `tree_to_array`를 활용함으로 보조해주는 재귀함수.

## RB Tree Visualize
```C
void print_tree(rbtree *t, node_t *node, int depth) {
  if (node == t->nil) {
    return;
  }

  print_tree(t, node->right, depth + 1);
  for (int i = 0; i < depth; i++) {
    printf("     ");
  }
  printf("R----%d (%s)\n", node->key, node->color == RBTREE_RED ? "Red" : "Black");
  print_tree(t, node->left, depth + 1);
}

// [MOD] debugging purposes (must be commented for 'make test')
int main(int argc, char *argv[]) {
  rbtree *t = new_rbtree();
  for(int i = 1; i < 11; i++) {
    rbtree_insert(t, i);
  }
  
  print_tree(t, t->root, 0);
  return 0;
}
```

실행시 콘솔에 아래와 같이 출력된다.

```text
                    R----10 (Red)
               R----9 (Black)
          R----8 (Red)
               R----7 (Black)
     R----6 (Black)
          R----5 (Black)
R----4 (Black)
          R----3 (Black)
     R----2 (Black)
          R----1 (Black)
```

뿅!

---

## 구현 범위
다음 기능들을 수행할 수 있도록 RB tree를 구현합니다.

- tree = `new_tree()`: RB tree 구조체 생성
  - 여러 개의 tree를 생성할 수 있어야 하며 각각 다른 내용들을 저장할 수 있어야 합니다.
- `delete_tree(tree)`: RB tree 구조체가 차지했던 메모리 반환
  - 해당 tree가 사용했던 메모리를 전부 반환해야 합니다. (valgrind로 나타나지 않아야 함)

- `tree_insert(tree, key)`: key 추가
  - 구현하는 ADT가 multiset이므로 이미 같은 key의 값이 존재해도 하나 더 추가 합니다.
- ptr = `tree_find(tree, key)`
  - RB tree내에 해당 key가 있는지 탐색하여 있으면 해당 node pointer 반환
  - 해당하는 node가 없으면 NULL 반환
- `tree_erase(tree, ptr)`: RB tree 내부의 ptr로 지정된 node를 삭제하고 메모리 반환
- ptr = `tree_min(tree)`: RB tree 중 최소 값을 가진 node pointer 반환
- ptr = `tree_max(tree)`: 최대값을 가진 node pointer 반환

- `tree_to_array(tree, array, n)`
  - RB tree의 내용을 *key 순서대로* 주어진 array로 변환
  - array의 크기는 n으로 주어지며 tree의 크기가 n 보다 큰 경우에는 순서대로 n개 까지만 변환
  - array의 메모리 공간은 이 함수를 부르는 쪽에서 준비하고 그 크기를 n으로 알려줍니다.

## 구현 규칙
- `src/rbtree.c` 이외에는 수정하지 않고 test를 통과해야 합니다.
- `make test`를 수행하여 `Passed All tests!`라는 메시지가 나오면 모든 test를 통과한 것입니다.
- Sentinel node를 사용하여 구현했다면 `test/Makefile`에서 `CFLAGS` 변수에 `-DSENTINEL`이 추가되도록 comment를 제거해 줍니다.


## 참고문헌
- [위키백과: 레드-블랙 트리](https://ko.wikipedia.org/wiki/%EB%A0%88%EB%93%9C-%EB%B8%94%EB%9E%99_%ED%8A%B8%EB%A6%AC)
([영어](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree))
- CLRS book (Introduction to Algorithms) 13장 레드 블랙 트리 - Sentinel node를 사용한 구현
- [Wikipedia:균형 이진 트리의 구현 방법들](https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree#Implementations)
