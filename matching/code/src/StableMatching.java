import java.util.*;

public class StableMatching {

    private static Map<Integer, String> men = new HashMap<>();
    private static Map<Integer, String> women = new HashMap<>();
    private static Map<Integer, List<Integer>> priorities = new HashMap<>();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();
        while (line.startsWith("#")) {
            line = scanner.nextLine();
        }
        // All women and men are free
        int n = Integer.parseInt(line.split("=")[1]);
        System.out.println("n: " + n);

        Map<String, String> pairs = new HashMap<>();

        for (int i = 1; i <= n * 2; i++) {
            String[] info = scanner.nextLine().split(" ");
            if(i % 2 == 0){
                women.put(Integer.parseInt((info[0])), info[1]);
            }else{
                men.put(Integer.parseInt((info[0])), info[1]);
            }
        }
        scanner.nextLine();
        for (int i = 0; i < n * 2; i++) {
            line = scanner.nextLine();
            priorities.put(i,
                    Arrays.stream(
                            line.split(": ")[1].split(" "))
                            .mapToInt(x -> Integer.parseInt(x))
                            .boxed().toList());
        }

        while (pairs.keySet().size() != n) { // while there is a free man
            for (Map.Entry<Integer, String> man : men.entrySet()) {
                if (pairs.keySet().contains(man.getKey())) continue;
                // get highest ranked woman for the man
                String w = getNextUnProposedWoman(man);
                if (!pairs.values().contains(w)) { // is this woman free?
                    pairs.put(man.getValue(), w);
                    priorities.get(man.getKey()).remove(0);
                } else {
                    if () { // if woman preferes this man to her engaged switch

                    } else {
                        priorities.get(man.getKey()).remove(0);
                    }
                }
            }
        }

        System.out.println(names);
        System.out.println(prioties);
    }

    private static String getNextUnProposedWoman (Map.Entry man) {
        return women.get(priorities.get(man.getKey()).get(0));
    }
}