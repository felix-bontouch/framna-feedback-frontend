import { AppType } from '@graphql'
import { Query, Resolver } from '@nestjs/graphql'
import { AppService } from '@service'

@Resolver()
export class AppsResolver {
  constructor(private readonly appService: AppService) {}

  @Query(returns => [AppType])
  async apps(): Promise<AppType[]> {
    return this.appService.findAll().map(i => ({
      ...i,
      icon: i.icon.startsWith('http') ? i.icon : `http://localhost:3000${i.icon}`
    }))
  }
}
