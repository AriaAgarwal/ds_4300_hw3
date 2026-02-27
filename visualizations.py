from fda_api import FDA_API

def create_visualizations(fda):
    recovered = fda.get_fatal_drugs(10, True, "1")
    #print(recovered)
    fatal = fda.get_fatal_drugs(10, True, "5")
    #print(fatal)

    common_reactions = fda.get_common_reactions_by_sex(10)
    print(common_reactions)




def main() :
    fda = FDA_API()
    create_visualizations(fda)


if __name__ == "__main__":
    main()